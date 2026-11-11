"""gNMI wire layer: path parsing and Get/Set on the vendored gNMI 0.10.0 protos.

pygnmi (0.8.x) still opens the channel and answers Capabilities, but it cannot
send ``union_replace``, cannot express a raw CLI path, and its path parser
splits CLI text on ``/``. Requests are built here instead and sent on the
pooled channel; responses are shaped like pygnmi's so existing consumers see the
same JSON.
"""

import json
import queue
import re
import threading
import time

import grpc

from grpc_driver.errors import DriverError
from grpc_driver.gnmi100 import gnmi_pb2 as pb

RAW_ORIGINS = ("cli",)
ENCODINGS = {"json": pb.JSON, "bytes": pb.BYTES, "proto": pb.PROTO, "ascii": pb.ASCII, "json_ietf": pb.JSON_IETF}
OP_NAMES = {1: "DELETE", 2: "REPLACE", 3: "UPDATE", 4: "UNION_REPLACE"}
UNION_REPLACE_MIN = (0, 10, 0)
_ORIGIN_PREFIX = re.compile(r"^/?([^:/\[\]\s]+):")


# ----------------------------------------------------------------------- paths

def _split_elements(text):
    """Split ``a/b[k=v][k2=v2]/c`` on ``/`` outside ``[...]``. Backslash escapes ``]``, ``[`` and ``\\``."""
    elems, name, keys, i, n = [], [], [], 0, len(text)

    def flush():
        if name or keys:
            elems.append(("".join(name), dict(keys)))
        name.clear()
        keys.clear()

    while i < n:
        ch = text[i]
        if ch == "\\" and i + 1 < n:
            name.append(text[i + 1])
            i += 2
        elif ch == "[":
            j, body = i + 1, []
            while j < n and text[j] != "]":
                if text[j] == "\\" and j + 1 < n:
                    body.append(text[j + 1])
                    j += 2
                else:
                    body.append(text[j])
                    j += 1
            if j >= n:
                raise DriverError(f"Invalid gNMI path '{text}': unterminated '['", "invalid_input")
            key, eq, value = "".join(body).partition("=")
            if not eq or not key:
                raise DriverError(f"Invalid gNMI path '{text}': key must look like [name=value]", "invalid_input")
            keys.append((key, value))
            i = j + 1
        elif ch == "/":
            flush()
            i += 1
        else:
            name.append(ch)
            i += 1
    flush()
    return elems


def parse_path(path, origin=None, raw=False, raw_origins=RAW_ORIGINS):
    """Build a gNMI Path.

    Accepted: ``/a/b[k=v]``; ``origin:/a/b`` and ``origin://`` (origin set, empty path);
    ``module:a/b`` (pygnmi compatible: the part before the first ``:`` is the origin);
    ``cli:show interface TenGigE0/0/0/3`` or ``origin='cli'`` (one verbatim element, never split or
    case-folded); and structured ``{"origin":..., "elem":[{"name":..., "key":{...}}]}`` or
    ``{"origin":..., "path": "..."}``. Case is always preserved.
    """
    if isinstance(path, dict):
        origin = path.get("origin", origin)
        if "elem" in path:
            out = pb.Path(origin=origin or "", target=path.get("target") or "")
            for e in path["elem"]:
                out.elem.add(name=e["name"], key={k: str(v) for k, v in (e.get("key") or {}).items()})
            return out
        out = parse_path(path.get("path", ""), origin=origin, raw=path.get("raw", raw), raw_origins=raw_origins)
        if path.get("target"):
            out.target = path["target"]
        return out

    text = "" if path is None else str(path).strip()
    out = pb.Path()
    match = _ORIGIN_PREFIX.match(text)
    explicit = match.group(1) if match else None
    effective = explicit or origin or ""
    if raw or effective in raw_origins:
        body = text[match.end():].lstrip("/") if match else text
        out.origin = effective
        if body:
            out.elem.add(name=body)
        return out
    out.origin = effective
    for name, key in _split_elements(text[match.end():] if match else text):
        out.elem.add(name=name, key=key)
    return out


def render_path(path):
    """pygnmi-style path text; an origin, when present, is kept as ``origin:/...``."""
    parts = []
    for e in path.elem:
        parts.append(e.name + "".join(f"[{k}={v}]" for k, v in sorted(e.key.items())))
    body = "/".join(parts)
    if path.origin:
        return f"{path.origin}:/{body}"
    return body or None


# ---------------------------------------------------------------------- values

def _json_bytes(value):
    if isinstance(value, (bytes, bytearray)):
        return bytes(value)
    if isinstance(value, str):
        try:
            json.loads(value)
            return value.encode()
        except ValueError:
            pass
    return json.dumps(value).encode()


def typed_value(value, encoding):
    enc = (encoding or "json_ietf").lower()
    if enc == "json":
        return pb.TypedValue(json_val=_json_bytes(value))
    if enc == "json_ietf":
        return pb.TypedValue(json_ietf_val=_json_bytes(value))
    if enc == "ascii":
        return pb.TypedValue(ascii_val=value if isinstance(value, str) else json.dumps(value))
    data = value.encode() if isinstance(value, str) else json.dumps(value).encode()
    if enc == "bytes":
        return pb.TypedValue(bytes_val=data)
    if enc == "proto":
        return pb.TypedValue(proto_bytes=data)
    raise DriverError(f"Unsupported encoding '{encoding}'", "invalid_input")


def _decode(tv):
    from pygnmi.client import process_potentially_json_value

    kind = tv.WhichOneof("value")
    if kind in ("json_ietf_val", "json_val"):
        return process_potentially_json_value(getattr(tv, kind))
    if kind == "leaflist_val":
        return [_decode(e) for e in tv.leaflist_val.element]
    if kind in ("decimal_val", "any_val"):
        return str(getattr(tv, kind))
    return getattr(tv, kind) if kind else None


# ---------------------------------------------------------------------- calls

def _pair(item, what):
    if isinstance(item, dict):
        path, value = item.get("path"), item.get("value")
    elif isinstance(item, (list, tuple)) and len(item) == 2:
        path, value = item
    else:
        raise DriverError(f"{what} entries must be [path, value] or {{path, value}}", "invalid_input")
    return path, value


def _updates(items, encoding, origin, raw, what):
    out = []
    for item in items or []:
        path, value = _pair(item, what)
        out.append(pb.Update(path=parse_path(path, origin, raw), val=typed_value(value, encoding)))
    return out


def _encoding(session, requested):
    name = (requested or getattr(session.gnmi, "_gNMIclient__encoding", None) or "json").lower()
    if name not in ENCODINGS:
        raise DriverError(f"encoding must be one of {sorted(ENCODINGS)}", "invalid_input")
    return name


def _rpc_error(session, exc):
    code = exc.code()
    return DriverError(
        f"GRPC ERROR Host: {session.spec.label()}, Error: {exc.details()}",
        code.name.lower(),
        evict=code in (grpc.StatusCode.UNAVAILABLE, grpc.StatusCode.UNAUTHENTICATED),
    )


def _unary(session, method, request, response_cls):
    key = ("callable", method)
    call = session.cache.get(key)
    if call is None:
        call = session.channel.unary_unary(
            f"/gnmi.gNMI/{method}",
            request_serializer=type(request).SerializeToString,
            response_deserializer=response_cls.FromString,
        )
        session.cache[key] = call
    try:
        return call(request, metadata=session.metadata, timeout=session.spec.rpc_timeout)
    except grpc.RpcError as exc:
        raise _rpc_error(session, exc)


def get(session, paths, datatype="all", encoding=None, prefix="", target=None, origin=None, raw=False):
    request = pb.GetRequest(
        prefix=parse_path(prefix, origin=None),
        path=[parse_path(p, origin, raw) for p in (paths or ["/"])],
        type=getattr(pb.GetRequest, datatype.upper()),
        encoding=ENCODINGS[_encoding(session, encoding)],
    )
    if target:
        request.prefix.target = target
    response = _unary(session, "Get", request, pb.GetResponse)
    out = {}
    if response.notification:
        out["notification"] = [notification_dict(n) for n in response.notification]
    return out


def notification_dict(n):
    """One gNMI Notification in pygnmi's JSON shape (shared by Get and Subscribe)."""
    item = {
        "timestamp": n.timestamp or 0,
        "prefix": render_path(n.prefix) if (n.prefix.elem or n.prefix.origin) else None,
        "alias": None,
        "atomic": n.atomic,
    }
    if n.update:
        item["update"] = [
            {"path": render_path(u.path) if (u.path.elem or u.path.origin) else None,
             **({"val": _decode(u.val)} if u.HasField("val") else {})}
            for u in n.update
        ]
    if n.delete:
        item["delete"] = [render_path(p) for p in n.delete]
    return item


def parse_version(text):
    try:
        return tuple(int(p) for p in str(text).split(".")[:3])
    except ValueError:
        return None


def device_version(session):
    if "gnmi_version" not in session.cache:
        caps = session.gnmi.capabilities() or {}
        session.cache["gnmi_version"] = caps.get("gnmi_version")
    return session.cache["gnmi_version"]


def require_union_replace(session):
    advertised = device_version(session)
    parsed = parse_version(advertised)
    if parsed is None or parsed < UNION_REPLACE_MIN:
        raise DriverError(
            f"{session.spec.label()} advertises gNMI {advertised or 'unknown'}; union_replace needs 0.10.0 or newer. "
            "An older target ignores the field and applies nothing. Pass force=true to send it anyway.",
            "unsupported",
        )


def set_(session, update=None, replace=None, union_replace=None, delete=None, encoding=None, prefix="",
         target=None, origin=None, raw=False, force=False):
    if union_replace and not force:
        require_union_replace(session)
    enc = _encoding(session, encoding)
    request = pb.SetRequest(
        prefix=parse_path(prefix),
        delete=[parse_path(p, origin, raw) for p in delete or []],
        replace=_updates(replace, enc, origin, raw, "replace"),
        update=_updates(update, enc, origin, raw, "update"),
        union_replace=_updates(union_replace, enc, origin, raw, "union_replace"),
    )
    if target:
        request.prefix.target = target
    response = _unary(session, "Set", request, pb.SetResponse)
    out = {
        "timestamp": response.timestamp or 0,
        "prefix": render_path(response.prefix) if (response.prefix.elem or response.prefix.origin) else None,
    }
    if response.response:
        out["response"] = [
            {"path": render_path(r.path) if (r.path.elem or r.path.origin) else None,
             "op": OP_NAMES.get(r.op, "UNDEFINED")}
            for r in response.response
        ]
    return out


# ------------------------------------------------------------------- subscribe

SUBSCRIBE_MODES = ("once", "poll", "stream")
STREAM_MODES = {"sample": pb.SAMPLE, "on_change": pb.ON_CHANGE, "target_defined": pb.TARGET_DEFINED}
LIST_MODES = {"once": pb.SubscriptionList.ONCE, "poll": pb.SubscriptionList.POLL, "stream": pb.SubscriptionList.STREAM}
NANOS = 1_000_000_000


def subscribe(session, mode, paths, *, duration=0, call_timeout=30, max_updates=1000, poll_count=1,
              poll_interval=1.0, stream_mode="sample", sample_interval=0, heartbeat_interval=0,
              suppress_redundant=False, updates_only=False, encoding=None, prefix="", target=None,
              origin=None, raw=False):
    """Run one bounded gNMI Subscribe and return the notifications it produced.

    ``once`` reads until the device's sync_response. ``poll`` sends ``poll_count`` Poll messages,
    ``poll_interval`` seconds apart, and reads one sync_response per poll. ``stream`` collects until
    ``duration`` seconds pass or ``max_updates`` notifications arrive, then cancels the RPC.
    ``stop_reason`` is ``complete``, ``duration``, ``max_updates`` or ``device_closed``.
    """
    if mode == "stream" and stream_mode not in STREAM_MODES:
        raise DriverError(f"stream_mode must be one of {sorted(STREAM_MODES)}", "invalid_input")
    sub_mode = STREAM_MODES[stream_mode] if mode == "stream" else pb.SAMPLE
    subs = [
        pb.Subscription(
            path=parse_path(p, origin, raw), mode=sub_mode,
            sample_interval=int(sample_interval * NANOS) if mode == "stream" else 0,
            suppress_redundant=bool(suppress_redundant) if mode == "stream" else False,
            heartbeat_interval=int(heartbeat_interval * NANOS) if mode == "stream" else 0,
        )
        for p in (paths or ["/"])
    ]
    sub_list = pb.SubscriptionList(
        prefix=parse_path(prefix), subscription=subs, mode=LIST_MODES[mode],
        encoding=ENCODINGS[_encoding(session, encoding)], updates_only=bool(updates_only),
    )
    if target:
        sub_list.prefix.target = target

    outbox = queue.Queue()
    outbox.put(pb.SubscribeRequest(subscribe=sub_list))

    def requests():
        while True:
            item = outbox.get()
            if item is None:
                return
            yield item

    call = session.channel.stream_stream(
        "/gnmi.gNMI/Subscribe",
        request_serializer=pb.SubscribeRequest.SerializeToString,
        response_deserializer=pb.SubscribeResponse.FromString,
    )
    stream = call(requests(), metadata=session.metadata, timeout=call_timeout)

    state = {"reason": None}
    notifications, syncs = [], 0

    def stop(reason):
        if state["reason"] is None:
            state["reason"] = reason
            stream.cancel()

    timer = None
    if mode == "stream":
        timer = threading.Timer(duration, stop, args=("duration",))
        timer.daemon = True
        timer.start()
    elif mode == "poll":
        def poller():
            for i in range(poll_count):
                if state["reason"]:
                    return
                outbox.put(pb.SubscribeRequest(poll=pb.Poll()))
                if i + 1 < poll_count:
                    time.sleep(poll_interval)
        threading.Thread(target=poller, daemon=True).start()

    try:
        for response in stream:
            kind = response.WhichOneof("response")
            if kind == "update":
                notifications.append(notification_dict(response.update))
                if mode == "stream" and len(notifications) >= max_updates:
                    stop("max_updates")
                    break
            elif kind == "sync_response":
                syncs += 1
                if mode == "once" or (mode == "poll" and syncs >= poll_count):
                    state["reason"] = state["reason"] or "complete"
                    break
            elif kind == "error":
                raise DriverError(f"GRPC ERROR Host: {session.spec.label()}, Error: {response.error.message}",
                                  "subscribe_error")
        else:
            state["reason"] = state["reason"] or ("complete" if mode == "once" else "device_closed")
    except grpc.RpcError as exc:
        if not (state["reason"] and exc.code() == grpc.StatusCode.CANCELLED):
            raise _rpc_error(session, exc)
    finally:
        if timer is not None:
            timer.cancel()
        outbox.put(None)
        stream.cancel()

    return {"notification": notifications, "sync_responses": syncs, "stop_reason": state["reason"] or "complete"}
