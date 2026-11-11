"""Operation, gNOI-service and plugin registries.

Everything the driver can do is registered here, so extending the driver means
dropping a module into ``plugins/`` (or listing it in ``GRPC_PLUGINS``) that
calls ``@operation`` / ``register_service`` / ``register_stub``.
"""

import importlib
import importlib.util
import os
import sys
from dataclasses import dataclass
from typing import Callable

OPERATIONS = {}
SERVICES = {}
STUBS = {}


@dataclass
class Operation:
    name: str
    fn: Callable
    idempotent: bool = False
    description: str = ""
    deadline: Callable = None


def operation(name, idempotent=False, description="", deadline=None):
    """Register ``fn(session, params) -> JSON-serialisable`` as operation ``name``.

    ``idempotent`` operations are retried once on a fresh channel when a reused
    pooled channel turns out to be dead; everything else fails fast so a
    config change or reboot is never replayed.

    ``deadline(params, spec) -> seconds`` overrides the connection's
    ``rpc_timeout`` for operations that legitimately run longer, such as a
    bounded gNMI Subscribe stream.
    """

    def wrap(fn):
        OPERATIONS[name] = Operation(name, fn, idempotent, description or (fn.__doc__ or "").strip(), deadline)
        return fn

    return wrap


def deadline_for(name, params, spec):
    """Seconds an operation may run: its own deadline, else the connection's ``rpc_timeout``."""
    op = OPERATIONS.get(name)
    if op is not None and op.deadline is not None:
        return op.deadline(params, spec)
    return spec.rpc_timeout


def register_service(alias, pb2_module, stub_cls, service_name):
    """Expose every RPC of a compiled gRPC service as ``<alias>.<Method>`` for the ``gnoi`` operation."""
    SERVICES[alias] = (pb2_module, stub_cls, service_name)


def register_stub(name, stub_cls):
    STUBS[name] = stub_cls


def _import_path(path):
    name = "grpc_plugin_" + os.path.splitext(os.path.basename(path))[0]
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)


def plugin_dirs(base_dir):
    dirs = [os.path.join(base_dir, "plugins")]
    extra = os.environ.get("GRPC_PLUGIN_DIR", "")
    dirs += [d for d in extra.split(os.pathsep) if d]
    return dirs


def load_plugins(base_dir):
    """Import built-in operation modules, then every plugin module."""
    for mod in ("grpc_driver.ops_gnmi", "grpc_driver.ops_gnoi", "grpc_driver.ops_subscribe", "grpc_driver.ops_reflect", "grpc_driver.ops_command", "grpc_driver.ops_cfgtext"):
        importlib.import_module(mod)
    for directory in plugin_dirs(base_dir):
        if not os.path.isdir(directory):
            continue
        for fname in sorted(os.listdir(directory)):
            if fname.endswith(".py") and not fname.startswith("_"):
                _import_path(os.path.join(directory, fname))
    for item in filter(None, (s.strip() for s in os.environ.get("GRPC_PLUGINS", "").split(","))):
        if item.endswith(".py") and os.path.isfile(item):
            _import_path(item)
        else:
            importlib.import_module(item)
