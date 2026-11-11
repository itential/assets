"""Pool daemon and its client.

Gateway 5 starts a fresh python process for every service call, so an
in-process pool can never outlive a call. The daemon is a small background
process that owns the pool; each one-shot call talks to it over a unix socket
(newline-delimited JSON), borrows a warm channel and exits. The daemon exits
by itself after ``GRPC_POOL_DAEMON_IDLE`` seconds with no channels.
"""

import fcntl
import hashlib
import json
import os
import socket
import socketserver
import subprocess
import sys
import tempfile
import threading
import time

from grpc_driver import registry
from grpc_driver.errors import classify
from grpc_driver.executor import execute_pooled
from grpc_driver.pool import ChannelPool
from grpc_driver.session import ConnSpec

PROTOCOL = 1
MAX_REQUEST = 16 * 1024 * 1024
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


class PoolUnavailable(Exception):
    """Nothing was sent: it is safe to fall back to a direct connection."""


class PoolError(Exception):
    """The request may have reached the daemon: never replay it on another path."""


def code_hash():
    """Hash of the driver code, so a re-pulled repo never talks to a daemon running old code."""
    digest = hashlib.sha1()
    paths = [os.path.join(BASE_DIR, "main.py")]
    for root in [os.path.join(BASE_DIR, "grpc_driver")] + registry.plugin_dirs(BASE_DIR):
        if os.path.isdir(root):
            paths += [os.path.join(root, f) for f in sorted(os.listdir(root)) if f.endswith(".py")]
    for path in paths:
        try:
            with open(path, "rb") as fh:
                digest.update(fh.read())
        except OSError:
            pass
    return digest.hexdigest()[:8]


def socket_path():
    path = os.environ.get("GRPC_POOL_SOCKET")
    if not path:
        # /tmp, not TMPDIR: unix socket paths are capped at ~104 bytes and macOS TMPDIR alone is ~50.
        base = "/tmp" if os.path.isdir("/tmp") else tempfile.gettempdir()
        directory = os.path.join(base, f"itential-grpc-pool-{os.getuid()}")
        try:
            os.makedirs(directory, mode=0o700, exist_ok=True)
            os.chmod(directory, 0o700)
        except OSError as exc:
            raise PoolUnavailable(f"cannot create socket directory {directory}: {exc}")
        path = os.path.join(directory, f"p-{code_hash()}.sock")
    if len(path.encode()) > 100:
        raise PoolUnavailable(f"socket path too long for AF_UNIX ({len(path)} bytes): {path}")
    return path


def _env_int(name, default):
    try:
        return int(os.environ.get(name, default))
    except ValueError:
        return default


class _Handler(socketserver.StreamRequestHandler):
    def handle(self):
        server = self.server
        server.touch()
        try:
            line = self.rfile.readline(MAX_REQUEST)
            request = json.loads(line)
            reply = server.dispatch(request)
        except Exception as exc:  # noqa: BLE001
            etype, message, _ = classify(exc)
            reply = {"ok": False, "error_type": etype, "error": message}
        self.wfile.write((json.dumps(reply, default=str) + "\n").encode())
        server.touch()


class PoolServer(socketserver.ThreadingMixIn, socketserver.UnixStreamServer):
    daemon_threads = True

    def __init__(self, path, pool, idle_exit):
        self.pool = pool
        self.idle_exit = idle_exit
        self.last_activity = time.time()
        self.started = time.time()
        self.path = path
        super().__init__(path, _Handler)
        os.chmod(path, 0o600)

    def touch(self):
        self.last_activity = time.time()

    def dispatch(self, request):
        if request.get("v") != PROTOCOL:
            return {"ok": False, "error_type": "protocol", "error": "protocol version mismatch"}
        op = request.get("op")
        if op == "__status__":
            status = self.pool.stats()
            status.update(pid=os.getpid(), uptime_s=round(time.time() - self.started), socket=self.path,
                          daemon_idle_exit_s=self.idle_exit)
            return {"ok": True, "result": status}
        if op == "__stop__":
            threading.Thread(target=self.shutdown, daemon=True).start()
            return {"ok": True, "result": {"stopping": True}}
        spec = ConnSpec.from_dict(request["conn"])
        try:
            result, meta = execute_pooled(self.pool, spec, op, request.get("params") or {})
            return {"ok": True, "result": result, "pool": meta}
        except Exception as exc:  # noqa: BLE001
            etype, message, _ = classify(exc)
            return {"ok": False, "error_type": etype, "error": message}


def _reaper(server, interval=10):
    while True:
        time.sleep(interval)
        server.pool.reap()
        idle = time.time() - server.last_activity
        if server.pool.size() == 0 and idle > server.idle_exit:
            server.shutdown()
            return


def serve():
    path = socket_path()
    lock = open(path + ".lock", "w")
    try:
        fcntl.flock(lock, fcntl.LOCK_EX | fcntl.LOCK_NB)
    except OSError:
        return  # another daemon already owns this socket
    if os.path.exists(path):
        os.unlink(path)  # stale socket from a crashed daemon; we hold the lock
    registry.load_plugins(BASE_DIR)
    pool = ChannelPool(
        max_size=_env_int("GRPC_POOL_MAX_SIZE", 32),
        idle_ttl=_env_int("GRPC_POOL_IDLE_TTL", 300),
        max_age=_env_int("GRPC_POOL_MAX_AGE", 3600),
    )
    server = PoolServer(path, pool, _env_int("GRPC_POOL_DAEMON_IDLE", 600))
    threading.Thread(target=_reaper, args=(server,), daemon=True).start()
    try:
        server.serve_forever()
    finally:
        pool.close_all()
        server.server_close()
        try:
            os.unlink(path)
        except OSError:
            pass


def _roundtrip(path, payload, timeout):
    with socket.socket(socket.AF_UNIX, socket.SOCK_STREAM) as sock:
        sock.settimeout(timeout)
        try:
            sock.connect(path)
        except OSError as exc:
            raise PoolUnavailable(str(exc))
        try:
            sock.sendall((json.dumps(payload) + "\n").encode())
            buf = b""
            while not buf.endswith(b"\n"):
                chunk = sock.recv(65536)
                if not chunk:
                    break
                buf += chunk
        except OSError as exc:
            raise PoolError(f"lost contact with the pool daemon mid-request: {exc}")
    if not buf:
        raise PoolError("pool daemon closed the connection without a reply")
    return json.loads(buf)


def _spawn(path):
    try:
        log = open(path + ".log", "a")
    except OSError as exc:
        raise PoolUnavailable(f"cannot open daemon log: {exc}")
    env = dict(os.environ, PYTHONPATH=BASE_DIR + os.pathsep + os.environ.get("PYTHONPATH", ""))
    subprocess.Popen(
        [sys.executable, "-m", "grpc_driver.poold"],
        cwd=BASE_DIR, env=env, stdin=subprocess.DEVNULL, stdout=log, stderr=log,
        start_new_session=True, close_fds=True,
    )


def request(payload, spawn=True, wait=5.0, timeout=60.0):
    """Send ``payload`` to the daemon, starting it if needed. Raises PoolUnavailable if it cannot be reached."""
    path = socket_path()
    payload = dict(payload, v=PROTOCOL)
    try:
        return _roundtrip(path, payload, timeout)
    except PoolUnavailable:
        if not spawn:
            raise
    _spawn(path)
    deadline = time.time() + wait
    while time.time() < deadline:
        time.sleep(0.1)
        try:
            return _roundtrip(path, payload, timeout)
        except PoolUnavailable:
            continue
    raise PoolUnavailable(f"pool daemon did not start within {wait}s (see {path}.log)")


if __name__ == "__main__":
    serve()
