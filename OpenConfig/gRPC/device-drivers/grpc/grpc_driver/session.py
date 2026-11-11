"""One authenticated gRPC channel to one device, plus the stubs built on top of it."""

import hashlib
import json
import threading
import time
from dataclasses import asdict, dataclass, field, fields

import grpc

from grpc_driver import registry
from grpc_driver.errors import DriverError

KEEPALIVE_OPTIONS = (
    ("grpc.keepalive_time_ms", 60000),
    ("grpc.keepalive_timeout_ms", 20000),
    ("grpc.keepalive_permit_without_calls", 1),
)
# gRPC's 4MB default rejects large running configs.
MESSAGE_SIZE_OPTIONS = (
    ("grpc.max_receive_message_length", 64 * 1024 * 1024),
    ("grpc.max_send_message_length", 64 * 1024 * 1024),
)
# Not part of a channel's identity: changing them must not open a second channel.
NON_IDENTITY_FIELDS = ("timeout", "rpc_timeout", "max_concurrent")


@dataclass(frozen=True)
class ConnSpec:
    host: str
    port: int = 57400
    username: str = ""
    password: str = ""
    insecure: bool = False
    skip_verify: bool = False
    path_cert: str = None
    path_key: str = None
    path_root: str = None
    override: str = None
    token: str = None
    timeout: int = 10        # seconds to establish the channel
    rpc_timeout: int = 30    # overall deadline for one operation
    max_concurrent: int = 8  # in-flight operations per host:port:user (devices cap sessions per user)
    grpc_options: tuple = field(default_factory=tuple)

    def key(self):
        """Pool key. Includes credentials so a rotated password never reuses a stale channel."""
        identity = {k: v for k, v in asdict(self).items() if k not in NON_IDENTITY_FIELDS}
        blob = json.dumps(identity, sort_keys=True, default=str)
        return hashlib.sha256(blob.encode()).hexdigest()

    def limit_key(self):
        return (self.host, self.port, self.username)

    def to_dict(self):
        d = asdict(self)
        d["grpc_options"] = [list(o) for o in self.grpc_options]
        return d

    @classmethod
    def from_dict(cls, data):
        known = {f.name for f in fields(cls)}
        data = {k: v for k, v in data.items() if k in known}
        data["grpc_options"] = tuple(tuple(o) for o in data.get("grpc_options", ()))
        return cls(**data)

    def label(self):
        return f"{self.host}:{self.port}"


class Session:
    """A connected channel. Safe to share between threads: gRPC multiplexes calls over one HTTP/2 connection."""

    def __init__(self, spec):
        self.spec = spec
        self.created = time.time()
        self.last_used = self.created
        self.uses = 0
        self.cache = {}  # per-channel memo (e.g. reflection descriptors)
        self._client = None
        self._stubs = {}
        self._state = None
        self._lock = threading.Lock()

    def open(self):
        from pygnmi.client import gNMIclient

        options = list(self.spec.grpc_options)
        have = {k for k, _ in options}
        options += [o for o in KEEPALIVE_OPTIONS + MESSAGE_SIZE_OPTIONS if o[0] not in have]
        try:
            client = gNMIclient(
                target=(self.spec.host, self.spec.port),
                username=self.spec.username,
                password=self.spec.password,
                insecure=self.spec.insecure,
                skip_verify=self.spec.skip_verify,
                path_cert=self.spec.path_cert,
                path_key=self.spec.path_key,
                path_root=self.spec.path_root,
                override=self.spec.override,
                token=self.spec.token,
                gnmi_timeout=self.spec.timeout,
                grpc_options=options,
            )
            client.connect(timeout=self.spec.timeout)
        except grpc.FutureTimeoutError:
            raise DriverError(
                f"Timed out after {self.spec.timeout}s connecting to {self.spec.label()}", "timeout"
            )
        self._client = client
        self.channel.subscribe(self._on_state, try_to_connect=False)
        return self

    def _on_state(self, state):
        self._state = state

    @property
    def gnmi(self):
        return self._client

    @property
    def channel(self):
        return self._client._gNMIclient__channel

    @property
    def metadata(self):
        return self._client._gNMIclient__metadata

    def healthy(self):
        return self._client is not None and self._state not in (
            grpc.ChannelConnectivity.TRANSIENT_FAILURE,
            grpc.ChannelConnectivity.SHUTDOWN,
        )

    def stub(self, name):
        with self._lock:
            if name not in self._stubs:
                cls = registry.STUBS.get(name)
                if cls is None:
                    raise DriverError(f"Unknown stub '{name}'", "unknown_stub")
                self._stubs[name] = cls(self.channel)
            return self._stubs[name]

    def close(self):
        client, self._client = self._client, None
        if client is not None:
            try:
                self.channel_unsubscribe(client)
                client.close()
            except Exception:
                pass

    def channel_unsubscribe(self, client):
        try:
            client._gNMIclient__channel.unsubscribe(self._on_state)
        except Exception:
            pass


def call_with_deadline(session, fn, seconds):
    """Run ``fn()`` and give up after ``seconds``.

    pygnmi issues RPCs without a deadline, so a wedged device would otherwise
    hang the process (or a pool thread) forever. On expiry the channel is
    closed, which cancels the in-flight RPC.
    """
    box = {}

    def target():
        try:
            box["result"] = fn()
        except BaseException as exc:  # noqa: BLE001 - re-raised in the caller
            box["error"] = exc

    worker = threading.Thread(target=target, daemon=True)
    worker.start()
    worker.join(seconds)
    if worker.is_alive():
        session.close()
        worker.join(2)
        raise DriverError(f"Operation exceeded the {seconds}s deadline", "timeout", evict=True)
    if "error" in box:
        raise box["error"]
    return box["result"]
