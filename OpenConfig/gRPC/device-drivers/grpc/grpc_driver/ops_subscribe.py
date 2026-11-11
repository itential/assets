"""gNMI Subscribe operations: ONCE, POLL and a bounded STREAM.

A Gateway 5 ``python-script`` service has to finish, so STREAM collects for ``duration`` seconds
(or ``max_updates`` notifications) and returns what it saw. Each operation declares its own deadline
because it legitimately outlives the connection's ``rpc_timeout``.
"""

import os

from grpc_driver import gnmi
from grpc_driver.errors import DriverError
from grpc_driver.ops_gnmi import as_bool, as_list
from grpc_driver.registry import operation

DEFAULT_DURATION = 10.0
DEFAULT_MAX_UPDATES = 1000
HARD_MAX_UPDATES = 100000


def _number(params, key, default, minimum=0.0, kind=float):
    raw = params.get(key)
    if raw in (None, ""):
        return default
    try:
        value = kind(raw)
    except (TypeError, ValueError):
        raise DriverError(f"{key} must be a number", "invalid_input")
    if value < minimum:
        raise DriverError(f"{key} must be >= {minimum}", "invalid_input")
    return value


def _max_duration():
    return float(os.environ.get("GRPC_SUBSCRIBE_MAX_DURATION", "300"))


def _common(params):
    return dict(
        paths=as_list(params.get("path")) or ["/"],
        encoding=params.get("encoding") or None,
        prefix=params.get("prefix") or "",
        target=params.get("target") or None,
        origin=params.get("origin") or None,
        raw=as_bool(params.get("raw")),
    )


def _poll_settings(params):
    return _number(params, "count", 1, minimum=1, kind=int), _number(params, "interval", 1.0)


def _stream_duration(params):
    duration = _number(params, "duration", DEFAULT_DURATION, minimum=0.1)
    if duration > _max_duration():
        raise DriverError(f"duration may not exceed {_max_duration():g}s (GRPC_SUBSCRIBE_MAX_DURATION)", "invalid_input")
    return duration


def _once_deadline(params, spec):
    return spec.rpc_timeout


def _poll_deadline(params, spec):
    count, interval = _poll_settings(params)
    return count * interval + spec.rpc_timeout


def _stream_deadline(params, spec):
    return _stream_duration(params) + spec.rpc_timeout


@operation("subscribe-once", idempotent=True, deadline=_once_deadline,
           description="gNMI Subscribe mode=ONCE: one snapshot, returned when the device sends sync_response")
def subscribe_once(session, params):
    return gnmi.subscribe(session, "once", call_timeout=session.spec.rpc_timeout,
                          updates_only=as_bool(params.get("updates_only")), **_common(params))


@operation("subscribe-poll", idempotent=True, deadline=_poll_deadline,
           description="gNMI Subscribe mode=POLL: `count` client-triggered polls, `interval` seconds apart")
def subscribe_poll(session, params):
    count, interval = _poll_settings(params)
    return gnmi.subscribe(session, "poll", poll_count=count, poll_interval=interval,
                          call_timeout=_poll_deadline(params, session.spec),
                          updates_only=as_bool(params.get("updates_only")), **_common(params))


@operation("subscribe-stream", idempotent=True, deadline=_stream_deadline,
           description="gNMI Subscribe mode=STREAM, collected for `duration` seconds or `max_updates` notifications")
def subscribe_stream(session, params):
    duration = _stream_duration(params)
    max_updates = _number(params, "max_updates", DEFAULT_MAX_UPDATES, minimum=1, kind=int)
    if max_updates > HARD_MAX_UPDATES:
        raise DriverError(f"max_updates may not exceed {HARD_MAX_UPDATES}", "invalid_input")
    return gnmi.subscribe(
        session, "stream",
        duration=duration, max_updates=max_updates,
        call_timeout=duration + session.spec.rpc_timeout,
        stream_mode=(params.get("stream_mode") or "sample").lower(),
        sample_interval=_number(params, "sample_interval", 0.0),
        heartbeat_interval=_number(params, "heartbeat_interval", 0.0),
        suppress_redundant=as_bool(params.get("suppress_redundant")),
        updates_only=as_bool(params.get("updates_only")),
        **_common(params),
    )
