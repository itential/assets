import grpc


class DriverError(Exception):
    """Raised for failures that should be reported as a structured error."""

    def __init__(self, message, error_type="driver_error", evict=False):
        super().__init__(message)
        self.error_type = error_type
        # True when the pooled channel that produced the error can no longer be trusted.
        self.evict = evict


def classify(exc):
    """Return (error_type, message, evict) for any exception raised by an operation."""
    if isinstance(exc, DriverError):
        return exc.error_type, str(exc), exc.evict
    wrapped = getattr(exc, "orig_exc", None)  # pygnmi wraps RpcError in gNMIException
    if isinstance(wrapped, grpc.RpcError):
        return classify(wrapped)
    if isinstance(exc, grpc.FutureTimeoutError):
        return "timeout", "Timed out establishing the gRPC channel", True
    if isinstance(exc, grpc.RpcError):
        code = exc.code() if callable(getattr(exc, "code", None)) else None
        name = code.name.lower() if code else "rpc_error"
        details = exc.details() if callable(getattr(exc, "details", None)) else str(exc)
        evict = code in (grpc.StatusCode.UNAVAILABLE, grpc.StatusCode.UNAUTHENTICATED)
        return name, f"{name}: {details}", evict
    return type(exc).__name__, str(exc), False
