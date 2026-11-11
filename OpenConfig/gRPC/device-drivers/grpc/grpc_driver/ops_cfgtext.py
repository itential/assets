"""Configuration Manager entry points that speak brace-style text (for Golden Config)."""

from grpc_driver import cfgtext, gnmi
from grpc_driver.errors import DriverError
from grpc_driver.ops_gnmi import as_bool, as_json, as_list
from grpc_driver.registry import operation


def _names(path):
    if not path:
        return []
    return [name + "".join(f"[{k}={v}]" for k, v in sorted(key.items())) for name, key in gnmi._split_elements(path)]


@operation("get-config-text", idempotent=True,
           description="Configuration as brace-style text, for Config Manager backups and Golden Config")
def get_config_text(session, params):
    response = gnmi.get(
        session,
        as_list(params.get("path")) or ["/"],
        datatype="config",
        encoding=params.get("encoding") or None,
        origin=params.get("origin") or None,
        raw=as_bool(params.get("raw")),
    )
    return cfgtext.render(cfgtext.tree_from_notifications(response, _names)) + "\n"


def _segment(line):
    return str(line).strip().strip("/")


@operation("set-config-text",
           description="Config Manager remediation with brace-text changes: [{parents, old, new}] applied as one gNMI Set")
def set_config_text(session, params):
    changes = as_json(params.get("config") or params.get("changes") or params.get("config_content"), "config")
    if not isinstance(changes, list) or not changes:
        raise DriverError("config must be a non-empty JSON array of {parents, old, new}", "invalid_input")
    mode = (params.get("mode") or "update").lower()
    if mode not in ("update", "replace", "union_replace"):
        raise DriverError("mode must be update, replace or union_replace", "invalid_input")
    apply, delete = [], []
    for change in changes:
        base = "/" + "/".join(_segment(p) for p in change.get("parents") or [] if _segment(p))
        new, old = change.get("new"), change.get("old")
        if new not in (None, ""):
            apply.append((base, cfgtext.parse(new)))
        elif old not in (None, ""):
            prefix = base.rstrip("/")
            delete.extend(f"{prefix}/{key}" for key in cfgtext.parse(old))
    if not (apply or delete):
        raise DriverError("no change had a 'new' value to apply or an 'old' value to delete", "invalid_input")
    gnmi.set_(session, **{mode: apply}, delete=delete,
              origin=params.get("origin") or None, force=as_bool(params.get("force")))
    return [{"result": True, "parents": c.get("parents") or [], "old": c.get("old") or "", "new": c.get("new")}
            for c in changes]
