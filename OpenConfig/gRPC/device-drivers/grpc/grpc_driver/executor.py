"""Run one operation against a session, with the retry rules that make pooling safe."""

from grpc_driver import registry
from grpc_driver.errors import DriverError, classify
from grpc_driver.session import Session, call_with_deadline


def run_on_session(session, op_name, params):
    op = registry.OPERATIONS.get(op_name)
    if op is None:
        raise DriverError(f"Unknown operation '{op_name}'. Available: {', '.join(sorted(registry.OPERATIONS))}",
                          "unknown_operation")
    seconds = registry.deadline_for(op_name, params, session.spec)
    return op, call_with_deadline(session, lambda: op.fn(session, params), seconds)


def execute_direct(spec, op_name, params):
    """One channel for exactly one operation (the Gateway 5 default when no pool is available)."""
    session = Session(spec).open()
    try:
        _, result = run_on_session(session, op_name, params)
        return result, {"mode": "direct", "reused": False}
    finally:
        session.close()


def execute_pooled(pool, spec, op_name, params):
    with pool.slot(spec):
        return _execute_pooled(pool, spec, op_name, params)


def _execute_pooled(pool, spec, op_name, params):
    """Lease a channel from ``pool``. A reused channel that turns out dead is replaced once, for idempotent ops only."""
    attempts = 2
    for attempt in range(attempts):
        session, reused = pool.acquire(spec)
        evict = False
        try:
            op, result = run_on_session(session, op_name, params)
            return result, {"mode": "pooled", "reused": reused}
        except Exception as exc:  # noqa: BLE001
            _, _, evict = classify(exc)
            retry = reused and evict and attempt + 1 < attempts and \
                registry.OPERATIONS.get(op_name) is not None and registry.OPERATIONS[op_name].idempotent
            if not retry:
                raise
        finally:
            pool.release(spec, session, evict=evict)
    raise AssertionError("unreachable")
