# trafficmorph — TrafficMorph Python SDK

```
████████╗██████╗  █████╗ ███████╗███████╗██╗ ██████╗
╚══██╔══╝██╔══██╗██╔══██╗██╔════╝██╔════╝██║██╔════╝
   ██║   ██████╔╝███████║█████╗  █████╗  ██║██║
   ██║   ██╔══██╗██╔══██║██╔══╝  ██╔══╝  ██║██║
   ██║   ██║  ██║██║  ██║██║     ██║     ██║╚██████╗
   ╚═╝   ╚═╝  ╚═╝╚═╝  ╚═╝╚═╝     ╚═╝     ╚═╝ ╚═════╝
        ███╗   ███╗ ██████╗ ██████╗ ██████╗ ██╗  ██╗
        ████╗ ████║██╔═══██╗██╔══██╗██╔══██╗██║  ██║
        ██╔████╔██║██║   ██║██████╔╝██████╔╝███████║
        ██║╚██╔╝██║██║   ██║██╔══██╗██╔═══╝ ██╔══██║
        ██║ ╚═╝ ██║╚██████╔╝██║  ██║██║     ██║  ██║
        ╚═╝     ╚═╝ ╚═════╝ ╚═╝  ╚═╝╚═╝     ╚═╝  ╚═╝
```

[![PyPI](https://img.shields.io/pypi/v/trafficmorph)](https://pypi.org/project/trafficmorph/)
[![Python versions](https://img.shields.io/pypi/pyversions/trafficmorph)](https://pypi.org/project/trafficmorph/)
[![License](https://img.shields.io/pypi/l/trafficmorph)](LICENSE)
[![Downloads](https://img.shields.io/pypi/dm/trafficmorph)](https://pypi.org/project/trafficmorph/)

Typed Python client for the TrafficMorph `/api/v1` API. Request
and response shapes are typed `attrs` classes; endpoint methods
expose both sync and async call styles.

## Install

```bash
# Quick start — always picks up the latest release.
pip install trafficmorph

# Reproducible builds (CI / production) — pin to an exact version.
pip install 'trafficmorph==0.3.0'
```

## Prerequisites

- **Python 3.10 or newer** — declared minimum in [`pyproject.toml`](pyproject.toml). Required for PEP 604 union syntax (`str | None`).
- **A TrafficMorph API key** in the form `tm_…`. Provision one from the in-app **Settings → API keys** page.
- **A reachable TrafficMorph install.** The examples below assume `http://localhost:8080` for local development; swap for your hosted URL otherwise. There is no built-in default — the SDK requires the base URL to be set explicitly.

## Quickstart

Export the two required values before running the program, so the snippet works as a single copy-paste:

```bash
export TM_API_KEY="tm_your_key_here"
export TM_BASE_URL="http://localhost:8080"   # or your hosted TrafficMorph URL
```

Then:

```python
import json
import os

from trafficmorph import Client
from trafficmorph.api.profiles import list_profiles

c = Client(
    api_key=os.environ["TM_API_KEY"],
    base_url=os.environ["TM_BASE_URL"],
    timeout=15.0,
)

resp = list_profiles.sync_detailed(client=c.api)
print(f"status: {resp.status_code}, {len(resp.content)} bytes")
```

### First successful call checklist

- [ ] `tm_…` API key exported as `TM_API_KEY` (or passed as the `api_key=` kwarg).
- [ ] `TM_BASE_URL` points at a reachable TrafficMorph server (`http://localhost:8080` for local dev).
- [ ] Program prints `status: 200, N bytes` — an empty profile list is `[]`, so N is typically ≥ 2.
- [ ] `resp.content` holds the JSON payload (bytes). Decode it per [Decoding responses](#decoding-responses) below.

If the program errored before reaching the first line, jump to [Common errors](#common-errors).

## Decoding responses

`resp.content` is the raw HTTP response body as `bytes`. Decode with `json` and the typed classes from `trafficmorph.models` — replace the `print(...)` line in the Quickstart with:

```python
from trafficmorph.models import TrafficProfileSummaryResponse

if resp.status_code == 200:
    profiles = [
        TrafficProfileSummaryResponse.from_dict(p)
        for p in json.loads(resp.content)
    ]
    for p in profiles:
        print(p.id, p.name)
elif resp.status_code in (400, 401, 403, 404):
    err = json.loads(resp.content)
    raise SystemExit(f"server returned {resp.status_code}: {err.get('error')}")
else:
    raise SystemExit(f"unexpected status {resp.status_code}: {resp.content!r}")
```

The `*.from_dict` classmethod on every model handles the OpenAPI optional-field semantics — missing fields become `attrs.NOTHING` so you don't get surprise `KeyError`s.

For status-code branching alone (without decoding), use `resp.status_code`. `resp.content` is the raw bytes; `resp.headers` is the response headers.

## Next steps

Three common flows after `list_profiles`:

### Create a profile

```python
from trafficmorph.api.profiles import create_profile
from trafficmorph.models import ApiProfileRequest, TrafficProfilePointRequest

body = ApiProfileRequest(
    name="smoke-test",
    target_url="https://api.example.com/health",
    http_method="GET",
    duration=60,
    points=[
        TrafficProfilePointRequest(x=0, y=10),
        TrafficProfilePointRequest(x=60, y=10),
    ],
)
resp = create_profile.sync_detailed(client=c.api, body=body)
```

### Start a run

```python
from trafficmorph.api.runs import start

# profile_id from list_profiles or create_profile
resp = start.sync_detailed(client=c.api, id=profile_id)
# resp.status_code == 200 → run started; poll get_profile for status.
```

### View recent history

```python
from trafficmorph.api.history import list_history

resp = list_history.sync_detailed(
    client=c.api,
    size=20,
    # Other optional filters: profile_id, triggered_by, region, auto_verdict, tag.
)
```

Every endpoint function exposes four call styles:

| Form | Returns |
|---|---|
| `endpoint.sync(client=…)` | Parsed body (currently `None` — see [Decoding responses](#decoding-responses)) |
| `endpoint.sync_detailed(client=…)` | `Response` with `.status_code`, `.content`, `.headers` |
| `endpoint.asyncio(client=…)` | Awaitable form of `sync` |
| `endpoint.asyncio_detailed(client=…)` | Awaitable form of `sync_detailed` |

For most cases, prefer `sync_detailed` / `asyncio_detailed` — they give you status code branching and the raw bytes for decoding.

## Common errors

All errors below come from `Client(...)` — they surface at construction time, before any network call, so you don't need to set up the rest of your app to hit them.

| Error fragment | Cause | Fix |
|---|---|---|
| `api_key must not be empty` | First arg to `Client` is `""` — usually a missing `TM_API_KEY` env var. | Pass the literal key or `export TM_API_KEY=...` before running. |
| `api_key: value contains a carriage return …` (or newline, NUL, DEL, other control byte) | API key has stray whitespace / control chars (a common copy-paste artifact). | Only the literal `tm_…` characters belong in the value; strip surrounding whitespace. |
| `base_url is required: pass base_url='http://…'` | No `base_url=` kwarg AND no `$TM_BASE_URL` env var. | Pass `base_url="http://..."` or export `TM_BASE_URL`. |
| `base URL "…" must include http:// or https:// scheme` | Base URL is missing the protocol (e.g. `localhost:8080`). | Add the scheme: `http://localhost:8080`. |
| `base URL "…" has scheme "…"; must be http or https` | Non-`http`/`https` scheme (e.g. `ftp://…`). | Use `http://` or `https://`. |
| `base URL "…" must not contain a query string` | Base URL has `?key=value` appended. | Strip the query — attach per-request params at the endpoint call site instead. |
| `base URL "…" must not contain a fragment` | Base URL has `#foo` appended. | Strip the fragment — fragments are client-side only and meaningless to the server. |
| `$TM_BASE_URL: …` (any of the above) | Env-supplied base URL fails the same checks. | Same fixes; the prefix names the source so you know whether the kwarg or the env var was at fault. |

## Configuration

| Source | Precedence |
|--------|------------|
| Constructor kwargs (`base_url=`, `timeout=`, …) | Highest |
| Environment variables (`TM_BASE_URL`) | Middle |
| Built-in defaults | Lowest |

| Kwarg | Env var | Default | Notes |
|---|---|---|---|
| `api_key` | — | _(required)_ | Full `tm_…` value. Empty string and header-invalid characters rejected upfront. |
| `base_url` | `TM_BASE_URL` | none — required | Points at your TrafficMorph install. See [Base URL rules](#base-url-rules) for accepted/rejected shapes. |
| `timeout` | — | `30.0` | Per-call timeout in seconds. Applied via `httpx.Timeout` on every request. |
| `user_agent` | — | `tm-python-sdk/<spec-version>` | Override to tag app traffic in HTTP logs (e.g. `"my-app/1.2.3 (tm-python-sdk/v1)"`). |
| `httpx_args` | — | `{}` | Extra kwargs forwarded to the underlying `httpx.Client` (proxies, mTLS, custom transports). |

### Base URL rules

Kwarg and env values are validated and normalized the same way, so they produce identical results for the same logical input. The kwarg wins on conflict.

**Accepted shapes** — any absolute `http://` or `https://` URL with a non-empty host:

- `http://localhost:8080` — typical local dev.
- `https://app.example.com` — hosted deployment.
- `https://host/proxy-prefix` — reverse-proxy mount; the prefix is preserved during URL resolution.
- `https://host/a%2Fb` — percent-encoded path segments stay verbatim. Per RFC 3986, `/a%2Fb` (one segment, containing a literal slash) and `/a/b` (two segments) are semantically different paths — the SDK never collapses one into the other.

The SDK appends a trailing slash if missing, so both spellings (with or without) produce the same final value.

**Rejected at construction time** — clear error from `Client(...)`, not a late transport failure:

| Bad input | Error fragment |
|---|---|
| `""` or whitespace-only | `must not be empty` |
| `localhost:8080` (no scheme) | `must include … scheme` |
| `ftp://x` (wrong scheme) | `must be http or https` |
| `https://` (no host) | `must include a host` |
| `https://x/?q=1` (query) | `must not contain a query string` |
| `https://x/#frag` (fragment) | `must not contain a fragment` |

Query strings and fragments are refused because they belong on per-request URLs, not the deployment root.

## Authentication

The SDK sends every request with `X-Api-Key: tm_…`. The API also accepts `Authorization: Bearer tm_…`, but the SDK uses `X-Api-Key`.

## What's in the box

```
trafficmorph                 ← public package (Client, env names, constants)
trafficmorph.api.<tag>       ← endpoint modules, one per OpenAPI tag
trafficmorph.models          ← typed request/response attrs classes
trafficmorph.errors          ← UnexpectedStatus exception
```

Endpoint coverage matches the server's `/api/v1` endpoints 1:1:

| Module | Endpoints |
|---|---|
| `trafficmorph.api.profiles` | `list_profiles`, `create_profile`, `get_profile`, `update_profile`, `delete_profile` |
| `trafficmorph.api.runs` | `start`, `stop`, `pause`, `resume` |
| `trafficmorph.api.history` | `list_history`, `get_history_item` |
| `trafficmorph.api.domains` | `list_`, `add`, `verify_dns`, `verify_http`, `remove` |
| `trafficmorph.api.captures` | `analyse`, `import_capture` |
| `trafficmorph.api.variables_sets` | `list_variables_sets`, `create`, `get`, `rename`, `change_mode`, `delete` |

## Versioning

| | Symbol | Meaning |
|---|---|---|
| SDK release | PyPI version (`pip install trafficmorph==X.Y.Z`) | Pin in your `requirements.txt` or `pyproject.toml` |
| API version | `trafficmorph.SPEC_VERSION` (currently `"v1"`) | The `/api/v1` revision this SDK targets |

Each SDK release targets one specific server `/api/v1` revision. The server preserves backwards compatibility within `/api/v1`, so SDK and server versions move independently — any released SDK version works against any TrafficMorph server still exposing `/api/v1`.
