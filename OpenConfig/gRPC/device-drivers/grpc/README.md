# grpc — Gateway 5 Python script service

gRPC driver for network devices: **gNMI** (Capabilities, Get, Set), **gNOI**
(System, Layer2, BGP, Interface) and **any other gRPC service** through server
reflection. It is one `main.py` with one service per operation, behavior
selected by an env var (`GRPC_OP`), and connection details taken from the
Inventory Manager record on stdin.

## Table of Contents

- [Config Manager services](#config-manager-services)
- [Prerequisites](#prerequisites)
- [Installing on a Gateway 5 server](#installing-on-a-gateway-5-server)
- [Inventory attributes](#inventory-attributes)
  - [Options](#options)
  - [Ports: `itential_port` and the gRPC port](#ports-itential_port-and-the-grpc-port)
- [Advanced services](#advanced-services)
  - [Connection and discovery](#connection-and-discovery)
  - [gNMI Get](#gnmi-get)
  - [gNMI Set](#gnmi-set)
  - [gNMI Subscribe](#gnmi-subscribe)
  - [gNOI](#gnoi)
- [Invocation model](#invocation-model)
- [Extending the driver](#extending-the-driver)
- [Connection pooling](#connection-pooling)
  - [What the pool guarantees](#what-the-pool-guarantees)
  - [Scope: per runner, not cross-server](#scope-per-runner-not-cross-server)
  - [Operating the pool](#operating-the-pool)
- [Output and errors](#output-and-errors)
- [Device behaviors handled](#device-behaviors-handled)
- [Local development](#local-development)

## Config Manager services

These are the services Inventory Manager and Config Manager need. Inventory
Manager maps its `is-alive`, `get-config`, `set-config` and `run-command` actions
to services by name, so these entry points keep their names, inputs and output
shapes. Do not rename them. Backups and Golden Config use the `-text` pair. The
mapping is in [Installing on a Gateway 5 server](#installing-on-a-gateway-5-server).

| Service | `GRPC_OP` | Purpose |
|---|---|---|
| `grpc-is-alive` | `is-alive` | Channel + gNMI Capabilities round trip. Prints bare `true` / `false`. |
| `grpc-gnmi-set-config` | `set-config` | Config Manager broker entry point. `config` is `[{parents, old, new}]`: `parents` joins into the path, `new` (JSON) is written, `old` with empty `new` deletes. `mode` = `update` (default), `replace` or `union_replace`; also `origin`, `force`. Returns `[{"result": true, ...}]` per change. |
| `grpc-gnmi-get-config-text` | `get-config-text` | Configuration as brace-style text, for Config Manager backups and Golden Config. Returns bare text. |
| `grpc-gnmi-set-config-text` | `set-config-text` | Config Manager remediation with brace-text changes (`[{parents, old, new}]` with text in `old` / `new`). Same `mode`, `origin`, `force` and result shape as `set-config`. |
| `grpc-run-command` | `run-command` | Config Manager / Command Templates entry point. `command` is newline-separated. Each line is `gnmi capabilities`, `gnmi get <path>`, `gnoi <service.Method> [json]`, or anything else, which is sent as a CLI-origin gNMI Get (e.g. `show version` on IOS XR). Returns `{success, host, results:[{command, output, success}]}`; one failing command does not hide the others. |

## Prerequisites

gNMI (and gNOI where you use it) enabled on the device and reachable from
Gateway 5. The driver runs on the host's default `python3`; dependencies install from `requirements.txt` via the
service's `runtime.req-file`.

**Large configurations:** Gateway 5 passes service inputs to Python scripts as command-line arguments, which Linux limits to about 128 KB each. On Gateway 5.5.3 or later, the `config` input of `grpc-gnmi-set-config` and `grpc-gnmi-set-config-text` is delivered to the driver as a file (path in `GRPC_CONFIG_FILE`), so full-device configurations larger than that limit are supported. This is declared on the `config` property in [`import.yaml`](import.yaml).

## Installing on a Gateway 5 server

**1. Create the Gateway 5 services.** Each operation is a
[Python script service](https://docs.itential.com/itential-gateway/5/iagctl/create-service-python-script).
[`import.yaml`](import.yaml) defines the repository, the input decorators and all 32
services. Copy this driver folder into your own Git repository, update the `repositories`
entry and each service's `working-directory` (`OpenConfig/gRPC/device-drivers/grpc`) to
match, then import it:

```bash
export GATEWAY_APPLICATION_MODE=client
iagctl db import import.yaml --force
```

You can also import the file from
[Gateway Manager](https://docs.itential.com/docs/gateway-manager) in Itential Platform.
The runner needs Python with network access to install `requirements.txt`, and a
route to each device's gNMI port (usually 57400).

**2. Set up Inventory Manager.** Add the connection attributes to each device
([Inventory attributes](#inventory-attributes)), then map the four actions to the
[Config Manager services](#config-manager-services)
(see [Inventory Manager](https://docs.itential.com/itential-platform/inventory-manager/overview)
and [Configuration Manager](https://docs.itential.com/itential-platform/configuration-manager/overview)):

| Inventory Manager action | Service |
|---|---|
| `is-alive` | `grpc-is-alive` |
| `get-config` | `grpc-gnmi-get-config-text` |
| `set-config` | `grpc-gnmi-set-config-text` |
| `run-command` | `grpc-run-command` |

`set-config` maps to the `-text` service because Config Manager sends configuration as
text. Map it to `grpc-gnmi-set-config` instead if your workflows send JSON changes.

## Inventory attributes

The minimum a node needs is a host, a port and credentials. This is enough for a
lab device or a first connection:

```json
{
  "name": "my-gnmi-device",
  "attributes": {
    "itential_host": "192.0.2.1",
    "itential_port": 57400,
    "itential_user": "username",
    "itential_password": "changeme"
  }
}
```

`insecure` is `false` by default, so the driver still connects with TLS. With no
certificate options set, it downloads the certificate the device presents when it
connects and trusts that one. The server is not checked against a certificate
authority, so for production set the certificate options. This node uses mutual TLS
with a CA, a client certificate and a client key, all read on the Gateway runner:

```json
{
  "name": "my-gnmi-device",
  "attributes": {
    "itential_host": "192.0.2.1",
    "itential_port": 57400,
    "itential_user": "username",
    "itential_password": "changeme",
    "itential_driver_options": {
      "grpc": {
        "path_root": "/etc/ssl/ca.pem",
        "path_cert": "/etc/ssl/client.pem",
        "path_key": "/etc/ssl/client.key"
      }
    }
  }
}
```

If the device certificate's name doesn't match the address you connect to, which is
common with self-signed certificates and IP addresses, set `override` or `skip_verify`.

Everything else goes under `itential_driver_options.grpc` and is optional. This
example connects to a lab device without TLS and turns on pooling:

```json
{
  "name": "my-gnmi-device",
  "attributes": {
    "itential_host": "192.0.2.1",
    "itential_port": 57400,
    "itential_user": "username",
    "itential_password": "changeme",
    "itential_driver_options": {
      "grpc": {
        "insecure": true,
        "pool": "auto",
        "rpc_timeout": 60
      }
    }
  }
}
```

### Options

| Attribute | Default | Description |
|---|---|---|
| `itential_host` | required | Device address. |
| `itential_port` | `57400` | Device port. See [Ports](#ports-itential_port-and-the-grpc-port) when the node is shared with another protocol. |
| `itential_user` / `itential_password` | required unless `token` is set | Credentials sent as gNMI metadata. |
| `grpc.port` | `itential_port` | gRPC port for this driver only. Takes precedence over `itential_port`. |
| `grpc.token` | none | Access token, used instead of a user and password. |
| `grpc.insecure` | `false` | Connect without TLS. |
| `grpc.skip_verify` | `false` | Accept a certificate whose name doesn't match the host, by using the certificate's own common name and subject alternative names as the target name. |
| `grpc.path_cert` | none | With no `path_key`, a certificate file to trust in place of the one downloaded from the device. With `path_key` and `path_root` as well, the client certificate for mutual TLS. |
| `grpc.path_key` / `grpc.path_root` | none | Client private key and CA certificate, used together with `path_cert` for mutual TLS. |
| `grpc.override` | none | Server name to use when checking the certificate, if it differs from the host. |
| `grpc.timeout` | `10` | Connect timeout in seconds. |
| `grpc.rpc_timeout` | `30` | Deadline in seconds for each operation. |
| `grpc.grpc_options` | keepalive and 64 MB message limits | Extra gRPC channel options, as an object or list of pairs, e.g. `{"grpc.max_send_message_length": 104857600}`. Values you set replace the defaults. |
| `grpc.pool` | `off` | Connection pooling mode: `off`, `auto` or `required`. See [Connection pooling](#connection-pooling). |
| `grpc.max_concurrent` | `8` | Most concurrent operations against one host, port and user. See [Connection pooling](#connection-pooling). |

Certificate paths are read on the Gateway runner, not on the Platform server.

### Ports: `itential_port` and the gRPC port

One inventory node can be reached over more than one protocol, depending on
which actions it is assigned. For example, Config Manager backups may use
`netmiko` (SSH, port 22) for some actions while `get-config` and `set-config`
use this driver (gNMI, typically 57400). Those protocols listen on different
ports, so a node can carry two:

- **`itential_port`** is the standard attribute shared by every driver on the
  node. Config Manager shows it in the Port field. For a node that is also
  managed over SSH it is usually `22`.
- **`itential_driver_options.grpc.port`** is the gRPC port for this driver only.

The driver picks the first of these that is set:

1. `--port` (local testing)
2. `itential_driver_options.grpc.port`
3. `itential_port`
4. `57400`

So set `grpc.port` whenever the node is shared with another protocol. If the
node is used only through this driver, `itential_port` alone is enough and
`grpc.port` can be left out. If `grpc.port` is missing on a shared node, the
driver will use the SSH port from `itential_port` and fail to connect.


## Advanced services

Beyond the Config Manager services, the driver registers one Gateway 5 service per
operation, 32 in total. They are optional and call the device directly from
workflows or `iagctl`, for cases Config Manager doesn't cover: connection checks,
explicit gNMI Get and Set, Subscribe, gNOI RPCs and reflection.
[`import.yaml`](import.yaml) is checked against the Python operation registry by
`tests/test_service_manifest.py`, so a service without an operation, or an
operation without a service, fails the test.

### Connection and discovery

| Service | `GRPC_OP` | Purpose |
|---|---|---|
| `grpc-gnmi-capabilities` | `capabilities` | gNMI Capabilities. |
| `grpc-reflection-call` | `call` | Any unary or server-streaming method via reflection: `method=gnoi.system.System/Time payload='{}'`. |
| `grpc-pool-status` / `grpc-pool-stop` | `pool-status` / `pool-stop` | Inspect or stop the pool daemon. |

### gNMI Get

Every Get takes `path` (repeatable), `encoding`, `prefix`, `target`, `origin` and `raw`.

| Service | `GRPC_OP` | Purpose |
|---|---|---|
| `grpc-gnmi-get` | `get` | gNMI Get with an explicit `datatype` (`all`, `config`, `state`, `operational`). |
| `grpc-gnmi-get-config` | `get-config` | Get type `CONFIG`. |
| `grpc-gnmi-get-state` | `get-state` | Get type `STATE`. |
| `grpc-gnmi-get-operational` | `get-operational` | Get type `OPERATIONAL`. |
| `grpc-gnmi-get-all` | `get-all` | Get type `ALL`. |

### gNMI Set

| Service | `GRPC_OP` | Purpose |
|---|---|---|
| `grpc-gnmi-set` | `set` | Generic Set: `update` / `replace` / `union_replace` as `[{path, value}]`, `delete` as `[path]`, plus `origin`, `raw`, `force`. Applied atomically by the device. `union_replace` (gNMI 0.10.0) is refused unless the device advertises 0.10.0+ (older targets silently ignore the field); `force=true` sends it anyway. |
| `grpc-gnmi-update-config` | `update-config` | Set with only `update[]` (merge). |
| `grpc-gnmi-replace-config` | `replace-config` | Set with only `replace[]`. |
| `grpc-gnmi-union-replace-config` | `union-replace-config` | Set with only `union_replace[]`. |
| `grpc-gnmi-delete-config` | `delete-config` | Set with only `delete[]`. |
| `grpc-gnmi-update-all` / `-replace-all` / `-union-replace-all` | `update-all` / `replace-all` / `union-replace-all` | The same verbs at the root path `/` with one `value`. **Require `confirm=true`**: a root replace rewrites the whole configuration, so the service refuses without it. |

The dedicated services accept only their own verb (plus `encoding`, `prefix`,
`target`, `origin`, `raw`, `force`), so a service named `update-config` can never
send a `replace`. None of the Set services are retried.

### gNMI Subscribe

Bounded by design: a `python-script` service has to finish, so nothing here
runs forever. Every Subscribe takes `path` (repeatable), `encoding`, `prefix`,
`target`, `origin`, `raw` and `updates_only`, and returns
`{"notification": [...], "sync_responses": n, "stop_reason": "..."}`.

| Service | `GRPC_OP` | Behavior |
|---|---|---|
| `grpc-gnmi-subscribe-once` | `subscribe-once` | Mode `ONCE`: one snapshot, returned when the device sends `sync_response`. |
| `grpc-gnmi-subscribe-poll` | `subscribe-poll` | Mode `POLL`: sends `count` Poll messages `interval` seconds apart and returns after `count` `sync_response`s. |
| `grpc-gnmi-subscribe-stream` | `subscribe-stream` | Mode `STREAM`: collects for `duration` seconds (default 10) or `max_updates` notifications (default 1000), then cancels. `stream_mode` is `sample` (default), `on_change` or `target_defined`; also `sample_interval`, `heartbeat_interval`, `suppress_redundant`. |

`stop_reason` is `complete` (ONCE and POLL finished), `duration`, `max_updates`
or `device_closed`. `duration` is capped by `GRPC_SUBSCRIBE_MAX_DURATION`
(default 300 s) and `max_updates` at 100000. These operations legitimately
outlive `rpc_timeout`, so each declares its own deadline (`duration` +
`rpc_timeout` for a stream) instead of being cut off at 30 s; the pool daemon
waits for it too. A Subscribe holds one `max_concurrent` slot for its whole
run, so keep streams short on devices with a tight session limit. They are
marked idempotent: a dead channel is retried once.

For POLL, the driver expects one `sync_response` for each Poll message it sends.

### gNOI

| Service | `GRPC_OP` | Purpose |
|---|---|---|
| `grpc-gnoi-call` | `gnoi` | Any gNOI RPC by name: `rpc=system.Time`, `rpc=layer2.ClearSpanningTree request='{...}'`. Streaming RPCs return a list (capped at 1000 messages). |
| `grpc-gnoi-time` | `gnoi-time` | `system.Time`. |
| `grpc-gnoi-ping` | `gnoi-ping` | `system.Ping`: `destination` (required), `source`, `count`, `interval`, `wait`, `size`, `do_not_fragment`, `do_not_resolve`, `l3protocol`. Replies come back as a list. |
| `grpc-gnoi-traceroute` | `gnoi-traceroute` | `system.Traceroute`: `destination` (required), `source`, `initial_ttl`, `max_ttl`, `wait`, `do_not_fragment`, `do_not_resolve`, `l3protocol`, `l4protocol`. |
| `grpc-gnoi-reboot` | `gnoi-reboot` | `system.Reboot` (`method`, `delay` ns, `message`). Never retried. |
| `grpc-gnoi-reboot-status` | `gnoi-reboot-status` | `system.RebootStatus`. |
| `grpc-gnoi-cancel-reboot` | `gnoi-cancel-reboot` | `system.CancelReboot` (`message`). Not retried. |

The ping, traceroute and reboot services build the request from the protobuf
descriptor, so each field above is the proto field name. Anything nested goes in
`request` as JSON; explicit inputs win over `request`.

These gNOI RPCs (ping, traceroute, reboot,
cancel_reboot, reboot_status, time, clear_lldp_interface, clear_bgp_neighbor,
clear_interface_counters, clear_neighbor_discovery, clear_spanning_tree,
wake_on_lan, switch_control_processor) are all reachable through `gnoi`, which
reads the protobuf service descriptors instead of needing a wrapper per RPC.
`grpc-gnoi-call` with a bad `rpc` lists every valid name.

**Software upload (`system.SetPackage`)** is a client-streaming RPC (package
metadata, then a stream of chunks, then a hash). The driver sends client-streaming
RPCs as a single message, so use the device's own tooling for image transfer.

## Invocation model

**One service per operation**, all pointing at `main.py` with a different
`GRPC_OP`. `import.yaml` registers them and their input schemas (booleans are
`"true"`/`"false"` strings; unset optional fields arrive as empty strings and
are ignored).

```bash
iagctl run service python-script grpc-is-alive
iagctl run service python-script grpc-gnmi-get --set path='["/interfaces/interface[name=eth0]/state"]' --set datatype=state
iagctl run service python-script grpc-gnoi-call --set rpc=system.Time
iagctl run service python-script grpc-reflection-call --set method=gnoi.system.System/Time
```

Inventory Manager action mapping:

```json
{
  "name": "get-config",
  "action_type": "iag5-service",
  "action_config": { "service_name": "grpc-gnmi-get-config", "cluster_id": "cluster-itential" },
  "action_parameters": {}
}
```

Connection flags (`--host --port --user --password --insecure --skip-verify
--path-cert --path-key --path-root --override --token --timeout --rpc-timeout
--pool`) override the inventory, for local testing:

```bash
python main.py --op get --host 192.0.2.1 --port 57400 --user username --password "$PW" --insecure true --path /
```

## Extending the driver

Everything is registered in `grpc_driver/registry.py`. Three extension points,
none of which touch the core:

**1. New operation.** Drop `plugins/<name>.py` (see `plugins/_example_plugin.py`):

```python
from grpc_driver.registry import operation

@operation("interface-counters", idempotent=True)
def interface_counters(session, params):
    return session.gnmi.get(path=[f"/interfaces/interface[name={params['name']}]/state/counters"], datatype="state")
```

`session` is a connected channel (`session.gnmi`, `session.channel`,
`session.metadata`, `session.stub(name)`); `params` are the `--key value` flags.
Mark `idempotent=True` only if replaying is safe. Add a service to `import.yaml`
with `GRPC_OP: interface-counters` and a decorator for its inputs. Pooling
works for plugin operations automatically.

**2. New gRPC service with compiled stubs.**
`register_service("healthz", healthz_pb2, healthz_pb2_grpc.HealthzStub, "Healthz")`
makes every RPC callable as `grpc-gnoi-call rpc=healthz.<Method>`.

**3. No stubs at all.** `grpc-reflection-call` works against any server with
reflection enabled. Descriptors are cached on the pooled channel, so repeat
calls skip the reflection round trips.

Plugin search path: `plugins/`, each directory in `GRPC_PLUGIN_DIR`
(`os.pathsep`-separated), and each module or `.py` file in `GRPC_PLUGINS`
(comma-separated).

The vendored `gnoi/` package holds the gNOI protobuf stubs.

## Connection pooling

Opening a channel costs a TCP connection, a TLS handshake and a Capabilities
round trip, and some devices cap concurrent sessions per user.

A `python-script` service is a fresh process per call, so a pool held inside
`main.py` is empty every time. Real pooling needs something that outlives the
call, so this driver ships one:

```
 Gateway 5 call 1 ─ python main.py ─┐
 Gateway 5 call 2 ─ python main.py ─┼─ unix socket ─▶ pool daemon ══ 1 warm HTTP/2 channel ══▶ device
 Gateway 5 call 3 ─ python main.py ─┘   (JSON lines)  (background)     per device identity
```

- **`off` (default)** — always a private channel, one connection per call.
  Pooling is opt-in because it needs a background daemon that outlives each
  script call, which not every Gateway 5 runtime allows.
- **`auto`** — use the daemon, starting it on first use. If it cannot be
  reached or started, fall back to a private channel for that one call. The
  result reports which happened (`--envelope true` → `pool.mode` = `pooled` |
  `fallback`, `pool.reused`).
- **`required`** — fail rather than fall back; use it when you want a broken
  pool to be loud.

Set it per device with `itential_driver_options.grpc.pool`, or globally with
the `GRPC_POOL` env var on the service. A `--pool` flag overrides both.

### What the pool guarantees

| Concern | Behavior |
|---|---|
| Pool key | `sha256` of host, port, credentials, TLS and gRPC options. A rotated password or changed option opens a new channel; it can never reuse a stale one. |
| Concurrency | One channel per key, shared. gRPC multiplexes concurrent calls over a single HTTP/2 connection, so a size-N pool per device would add nothing. |
| Liveness | Channel state is tracked; unhealthy channels are replaced. Keepalive pings (60 s) are on by default. |
| Dead channel | A call on a *reused* channel that fails with `UNAVAILABLE` / `UNAUTHENTICATED` evicts it and is retried once on a fresh one — **only for operations marked idempotent** (get, capabilities, is-alive, time, ...). `set`, `set-config`, the dedicated Set services, `gnoi-reboot` and anything else are never replayed. |
| Hung device | pygnmi sets no per-RPC deadline, so every operation runs under `rpc_timeout` (default 30 s); Subscribe operations declare a longer deadline of their own (see [gNMI Subscribe](#gnmi-subscribe)). On expiry the channel is closed, which cancels the in-flight RPC, and the channel is evicted. |
| Lifecycle | Idle channels close after `GRPC_POOL_IDLE_TTL` (300 s); channels are recycled after `GRPC_POOL_MAX_AGE` (3600 s); the daemon exits after `GRPC_POOL_DAEMON_IDLE` (600 s) with no channels; `GRPC_POOL_MAX_SIZE` (32) evicts least-recently-used idle channels. |
| Ambiguous failure | If the daemon dies *after* receiving a request, the call fails instead of falling back — a config push is never run twice. Fallback only happens when nothing was sent. |
| Code updates | The socket name includes a hash of the driver code, so a re-pulled repo gets a fresh daemon. Old ones idle out. |
| Security | Socket directory is `0700` and the socket `0600` (same uid only). Credentials sit in daemon memory for the life of a channel and are never written to disk. Logs go to `<socket>.log`. |

### Scope: per runner, not cross-server

**This is per-runner pooling, not a cross-server or cross-runner solution.**
The daemon is local to the host or container where the script executes, and
it is reached over a unix socket, so two runners can never share a channel.

| Gateway 5 topology | Pool | What a device sees |
|---|---|---|
| Single gateway, embedded runner | One daemon | 1 channel, up to `max_concurrent` operations in flight |
| Server plus separate runners (shared or physical hosts) | One daemon per runner host. The server executes nothing, so it holds no pool. | One channel per runner that touches the device |
| Virtual cluster, containerized runners | One daemon per runner container, lost when the container restarts or scales in (a cold reconnect, harmless) | One channel per runner replica |

Consequences:

- **Pooling still pays off.** Within one runner, repeat calls skip the TCP,
  TLS and Capabilities round trip, and a burst of calls shares one channel
  instead of opening one per call.
  The saving is smaller when devices are spread thinly across many runners,
  because each runner warms its own channel.
- **`max_concurrent` is per daemon, not global.** Devices cap sessions per
  user across all runners. With N runners that can reach a device, it can see
  up to N × `max_concurrent` operations in flight. Set `max_concurrent` to the
  device's limit divided by N.
- **Runner placement decides the hit rate.** If Gateway 5 spreads one device's
  jobs across runners, each runner opens its own channel and the device sees
  one source per runner. Pin devices to runners where you can.
- **No coordination between runners.** There is no shared state, lock or
  global session budget. If you need one, put a shared proxy in front of the
  devices instead of extending the pool.
- Tune `GRPC_POOL_*` on each runner. Keep `GRPC_POOL_IDLE_TTL` below any idle
  timeout on the device or a firewall.

### Operating the pool

- **Confirm the daemon persists between calls.** It is started
  detached (`start_new_session`). If your Gateway 5 runtime ends child
  processes when a script exits, `auto` falls back to one channel per call.
  To check on your deployment:

  ```bash
  iagctl run service python-script grpc-gnmi-get --set path='["/"]'   # twice, against a device
  iagctl run service python-script grpc-pool-status                    # hits should be 1, uses 2
  ```

  `running: false` after a call means the runtime killed it; set `GRPC_POOL=off`
  (the default) to stop paying for the spawn attempt, or run the daemon as a real service
  (`python -m grpc_driver.poold` under systemd or as a sidecar container, with
  `GRPC_POOL_SOCKET` pointing at a shared volume).
- Credentials are passed to the daemon per request, so the daemon holds a
  password for as long as the channel is alive.
- Unix sockets are capped at ~104 bytes; the default path is under `/tmp` for
  that reason.

## Output and errors

- Success: the operation's result as JSON on stdout, exit `0`.
  `is-alive` prints bare `true`/`false` (no newline) for gw-manager.
- Failure: exit `1`, the envelope on stderr
  (`success`, `op`, `host`, `device_name`, `error`, `error_type`, `pool`).
  `error_type` is the lower-cased gRPC status (`unavailable`, `unauthenticated`,
  `unimplemented`, ...) or `timeout` / `invalid_input` / `unknown_rpc` — the
  same distinctions an HTTP client would see as 408, 501 or security errors.
- `--envelope true` prints the full envelope on success too.

## Device behaviors handled

- **`union_replace`**: replaces the whole config with the union of its updates; the driver refuses it against gNMI < 0.10.0 (unless `force`).
- **Native / multi-origin paths** (`origin:/path`, `cli:` text, prefix/path origin mismatch).
- **CLI paths** with `/` in interface names and mixed case: never split or case-folded.
- **Boolean and numeric Set values**.
- **Large payloads**: 64 MB send/receive message limits by default (stock pygnmi fails at 4 MB).
- **Session limits**: pooled mode keeps one peer; `max_concurrent` (default 8, per host:port:user) rejects with `busy` rather than exhausting the device.
- **Reboot subcomponents**.

## Local development

```bash
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt pytest pyyaml
python -m pytest tests -q
```

`tests/test_service_manifest.py` checks that every service in `import.yaml` names a
registered operation, and the reverse. The driver itself does not import `pyyaml`.
