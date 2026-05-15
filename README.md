# trafficmorph — TrafficMorph Python SDK

Typed Python client for the TrafficMorph `/api/v1` surface.
Generated from the same versioned OpenAPI snapshot as the
[`tm` CLI](../cli/) and the [Go SDK](../sdk-go/) so all three stay
in lockstep.

```
pip install trafficmorph
```

## Quickstart

```python
import json

from trafficmorph import Client
from trafficmorph.api.profiles import list_profiles

c = Client(api_key="tm_xxxxxxxxxxxxxxxx")

resp = list_profiles.sync_detailed(client=c.api)
if resp.status_code == 200:
    # NOTE: resp.parsed is currently None for every 2xx response
    # — the server's `@ApiResponse` annotations don't declare body
    # schemas yet, so openapi-python-client can't auto-decode. Decode
    # the raw bytes via `json` instead. A future SDK release will
    # gain typed responses when the spec adds response schemas; the
    # wire contract itself isn't changing.
    for profile in json.loads(resp.content):
        print(profile["id"], profile["name"])
else:
    print(f"server returned {resp.status_code}: {resp.content!r}")
```

The endpoint functions live in `trafficmorph.api.<tag>` modules,
one per OpenAPI tag:

| Module | Endpoints |
|---|---|
| `trafficmorph.api.profiles` | `list_profiles`, `create_profile`, `get_profile`, `update_profile`, `delete_profile` |
| `trafficmorph.api.runs` | `start`, `stop`, `pause`, `resume` |
| `trafficmorph.api.history` | `list_history`, `get_history_item` |
| `trafficmorph.api.domains` | `list`, `add`, `verify_dns`, `verify_http`, `remove` |
| `trafficmorph.api.captures` | `analyse`, `import_capture` |

Each function exposes four call styles:

| Function form | Returns |
|---|---|
| `endpoint.sync(client=...)` | Currently `None` (see caveat below); intended to be the parsed body |
| `endpoint.sync_detailed(client=...)` | A `Response[T]` with `.status_code`, `.content` (raw bytes), and `.parsed` (currently `None`) |
| `endpoint.asyncio(client=...)` | Awaitable form of `sync` |
| `endpoint.asyncio_detailed(client=...)` | Awaitable form of `sync_detailed` |

**Caveat on `parsed`.** The current OpenAPI snapshot doesn't
declare body schemas on `@ApiResponse` annotations — only
descriptions and status codes. With no schema, openapi-python-client
can't generate auto-decode logic, so `parsed` is `None` on every
response (2xx and 4xx alike). Callers should use `sync_detailed`
and decode `resp.content` via `json.loads`. The wire contract is
documented in the OpenAPI spec; a future SDK release will gain
typed responses when the server-side annotations add `content =
@Content(schema = @Schema(...))` to declare each endpoint's body
shape.

Pick `sync_detailed` for everything today — it gives you the
status code (essential for branching on 4xx error envelopes the
server emits as `{"error": "..."}`) and the raw bytes for manual
decode.

## Authentication

The SDK injects an `X-Api-Key: tm_…` header on every request. The
alternative `Authorization: Bearer tm_…` form documented for the
public API works too — both schemes map to the same backing
filter server-side — but the SDK uses `X-Api-Key` because it
disambiguates from JWT / OAuth in access logs.

Provision the key from the in-app **Settings → API keys** page.

On the cloud build, API access is a TEAM+ feature. Self-hosted
installs (`app.deployment-mode=SELF_HOSTED`) give every
authenticated user full access regardless of stored plan tier.

## Configuration

| Source | Precedence |
|--------|------------|
| Constructor kwargs (`base_url=`, `timeout=`, …) | Highest |
| Environment variables (`TM_BASE_URL`) | Middle |
| Built-in defaults | Lowest |

| Kwarg | Env var | Default | Notes |
|---|---|---|---|
| `api_key` | — | _(required)_ | Full `tm_…` value. Empty string rejected. |
| `base_url` | `TM_BASE_URL` | `https://app.trafficmorph.example.com` | Either spelling (with/without trailing slash) works; SDK normalizes to a trailing-slash form so path-prefixed reverse-proxy deployments keep their prefix. |
| `timeout` | — | `30.0` | Per-call timeout in seconds. Applied via `httpx.Timeout`. |
| `user_agent` | — | `tm-python-sdk/v1` | Override to tag app traffic in server logs (e.g. `"my-app/1.2.3 (tm-python-sdk/v1)"`). |
| `httpx_args` | — | `{}` | Extra kwargs forwarded to the underlying `httpx.Client` — proxies, mTLS, custom transports. |

## Reaching the typed DTOs

Every request / response shape from the OpenAPI spec is a typed
`attrs` class under `trafficmorph.models`:

```python
from trafficmorph import Client
from trafficmorph.api.profiles import create_profile
from trafficmorph.models import (
    ApiProfileRequest,
    TrafficProfilePointRequest,
)

c = Client(api_key="tm_...")
req = ApiProfileRequest(
    name="smoke-test",
    target_url="https://api.example.com/health",
    http_method="GET",
    duration=60,
    points=[
        TrafficProfilePointRequest(x=0, y=10),
        TrafficProfilePointRequest(x=60, y=10),
    ],
)
resp = create_profile.sync_detailed(client=c.api, body=req)
# Same caveat as the Quickstart: `resp.parsed` is currently None
# until the server's @ApiResponse annotations declare body schemas.
# Decode `resp.content` via `json.loads` for now.
print(resp.status_code, resp.content)
```

## Versioning

| | Symbol | Meaning |
|---|---|---|
| SDK release | `pip install trafficmorph==0.1.0` | Bumped per release |
| Spec snapshot | `trafficmorph.SPEC_VERSION` (currently `"v1"`) | Tracks which `/api/v1` revision the SDK was generated against |

A given SDK release builds against one OpenAPI snapshot. Server-
side `/api/v1` changes always preserve backwards compatibility
within the v1 line — a 0.3.0 SDK works against the same server as
0.1.0, as long as both target `/api/v1`.

## Regenerating after a server-side API change

```
make -C cli regen-spec          # writes ../cli/openapi/v1.json
make -C sdk-python regen-client # regenerates trafficmorph/ in place
make -C sdk-python test
```

Then commit the snapshot + regenerated source in the same PR.

### Layout — what regen touches vs. what it doesn't

| Path | Owner | Touched by regen? |
|---|---|---|
| `trafficmorph/__init__.py` | Generator, with a post-step append | ✅ Overwritten — then patched to append `from .sdk import Client` |
| `trafficmorph/client.py`, `errors.py`, `types.py` | Generator | ✅ Overwritten |
| `trafficmorph/api/`, `trafficmorph/models/` | Generator | ✅ Overwritten |
| `trafficmorph/sdk.py` | Hand-written wrapper | ❌ Never touched by regen |
| `tests/`, `pyproject.toml`, `Makefile`, this README | Hand-written | ❌ Never touched by regen |

The generator's relative-imports (`from ...client import ...`)
require it to own `trafficmorph/` outright — moving the generated
code to a sub-package broke those imports. The wrapper sits in
its own file (`sdk.py`) so it survives `--overwrite`, and the
Makefile re-applies the `from .sdk import Client` re-export to
`__init__.py` after every regen.

Do NOT hand-edit anything other than `sdk.py` under
`trafficmorph/`; changes get clobbered.

## See also

- [`tm` CLI](../cli/) — single-binary wrapper for CI gating
- [Go SDK](../sdk-go/) — typed client for Go consumers
- [OpenAPI spec](../cli/openapi/v1.json) — canonical `/api/v1` snapshot
- Server-side docs at `/swagger-ui` on any TrafficMorph deployment
