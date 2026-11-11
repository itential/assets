"""Channel pool: one long-lived, multiplexed gRPC channel per device identity."""

import contextlib
import threading
import time

from grpc_driver.errors import DriverError
from grpc_driver.session import Session


class _Limit:
    def __init__(self, size):
        self.size = size
        self.sem = threading.BoundedSemaphore(size)
        self.in_flight = 0
        self.waiting = 0
        self.rejected = 0


class ChannelPool:
    def __init__(self, max_size=32, idle_ttl=300, max_age=3600, factory=Session):
        self.max_size = max_size
        self.idle_ttl = idle_ttl
        self.max_age = max_age
        self._factory = factory
        self._sessions = {}   # key -> Session
        self._leases = {}     # key -> in-flight operations
        self._key_locks = {}  # key -> lock serialising channel creation
        self._limits = {}     # (host, port, user) -> _Limit
        self._lock = threading.Lock()
        self.hits = 0
        self.misses = 0

    def acquire(self, spec):
        """Return (session, reused). Creates and connects a channel on first use."""
        key = spec.key()
        with self._lock:
            key_lock = self._key_locks.setdefault(key, threading.Lock())
        with key_lock:
            with self._lock:
                session = self._sessions.get(key)
                if session and self._usable(session):
                    self._lease(key, session)
                    self.hits += 1
                    return session, True
                stale = self._sessions.pop(key, None)
            if stale:
                stale.close()
            session = self._factory(spec).open()  # connect outside the global lock
            with self._lock:
                self.misses += 1
                self._make_room(exclude=key)
                self._sessions[key] = session
                self._lease(key, session)
            return session, False

    @contextlib.contextmanager
    def slot(self, spec, wait=None):
        """Bound concurrent operations per host:port:user so a burst never exceeds the device's session limit."""
        with self._lock:
            limit = self._limits.setdefault(spec.limit_key(), _Limit(max(1, int(spec.max_concurrent))))
            limit.waiting += 1
        wait = spec.rpc_timeout if wait is None else wait
        got = limit.sem.acquire(timeout=wait)
        with self._lock:
            limit.waiting -= 1
            if got:
                limit.in_flight += 1
            else:
                limit.rejected += 1
        if not got:
            raise DriverError(
                f"{spec.label()} already has {limit.size} operations in flight for user '{spec.username}'; "
                f"gave up waiting after {wait}s",
                "busy",
            )
        try:
            yield
        finally:
            with self._lock:
                limit.in_flight -= 1
            limit.sem.release()

    def release(self, spec, session, evict=False):
        key = spec.key()
        with self._lock:
            self._leases[key] = max(0, self._leases.get(key, 1) - 1)
            session.last_used = time.time()
            current = self._sessions.get(key) is session
            if evict and current:
                del self._sessions[key]
        if evict or not current:
            session.close()

    def _lease(self, key, session):
        self._leases[key] = self._leases.get(key, 0) + 1
        session.last_used = time.time()
        session.uses += 1

    def _usable(self, session):
        return session.healthy() and (time.time() - session.created) < self.max_age

    def _make_room(self, exclude):
        while len(self._sessions) >= self.max_size:
            idle = [(s.last_used, k) for k, s in self._sessions.items()
                    if k != exclude and not self._leases.get(k)]
            if not idle:
                return  # everything is busy; allow a temporary overshoot rather than fail
            _, victim = min(idle)
            self._sessions.pop(victim).close()

    def reap(self):
        """Close idle or unhealthy channels. Returns how many were closed."""
        now = time.time()
        with self._lock:
            doomed = [k for k, s in self._sessions.items()
                      if not self._leases.get(k) and (
                          now - s.last_used > self.idle_ttl or not self._usable(s))]
            sessions = [self._sessions.pop(k) for k in doomed]
        for s in sessions:
            s.close()
        return len(sessions)

    def close_all(self):
        with self._lock:
            sessions, self._sessions = list(self._sessions.values()), {}
        for s in sessions:
            s.close()

    def size(self):
        with self._lock:
            return len(self._sessions)

    def stats(self):
        now = time.time()
        with self._lock:
            return {
                "channels": [
                    {
                        "target": s.spec.label(),
                        "username": s.spec.username,
                        "key": k[:8],
                        "age_s": round(now - s.created),
                        "idle_s": round(now - s.last_used),
                        "uses": s.uses,
                        "in_flight": self._leases.get(k, 0),
                        "healthy": s.healthy(),
                    }
                    for k, s in self._sessions.items()
                ],
                "limits": [
                    {"target": f"{h}:{p}", "username": u, "max_concurrent": l.size,
                     "in_flight": l.in_flight, "waiting": l.waiting, "rejected": l.rejected}
                    for (h, p, u), l in self._limits.items()
                ],
                "hits": self.hits,
                "misses": self.misses,
                "max_size": self.max_size,
                "idle_ttl_s": self.idle_ttl,
                "max_age_s": self.max_age,
            }
