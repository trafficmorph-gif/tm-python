"""Hand-written ergonomic wrapper for the TrafficMorph Python SDK.

This file is **NOT** touched by ``make regen-client``. The generator
overwrites everything else under ``trafficmorph/`` (client.py,
errors.py, types.py, api/, models/) — keeping the wrapper here
keeps it regen-safe.

The public surface is re-exported through ``trafficmorph.__init__``
so callers do::

    from trafficmorph import Client
    from trafficmorph.api.profiles import list_profiles

without having to know about the wrapper-vs-generated split.
"""

import os
from typing import Any

import httpx

# Generator's `AuthenticatedClient` is the workhorse — httpx-based
# attrs class that we hand to the generated endpoint functions via
# the `client=` kwarg. Importing it under an underscore name keeps
# our public surface unambiguous: `Client` (defined below) is OUR
# wrapper, the generator's class is an implementation detail.
from .client import AuthenticatedClient as _AuthenticatedClient

__all__ = (
    "Client",
    "SPEC_VERSION",
    "DEFAULT_BASE_URL",
    "DEFAULT_USER_AGENT",
    "DEFAULT_TIMEOUT",
    "EnvBaseURL",
    "EnvAPIKey",
)

#: Which ``/api/v1`` snapshot this build was generated against.
#: Bumped manually alongside ``make -C cli regen-spec``.
SPEC_VERSION = "v1"

#: Default User-Agent sent on every request when the caller doesn't
#: override via ``user_agent``. Includes both the SDK name AND the
#: spec version so server-side observability can correlate client
#: revisions to API surface revisions.
DEFAULT_USER_AGENT = f"tm-python-sdk/{SPEC_VERSION}"

#: Fallback API base URL when neither ``base_url=`` nor
#: ``$TM_BASE_URL`` is set. Points at the SaaS instance; on-prem
#: callers always need to override.
DEFAULT_BASE_URL = "https://app.trafficmorph.example.com"

#: Default per-call HTTP timeout in seconds. Generous enough for
#: the heaviest v1 endpoint (``GET /history?…&size=100``) on a
#: slow-network laptop.
DEFAULT_TIMEOUT = 30.0

#: Env-var name for the API base URL. Matches the CLI / Go SDK
#: convention so a CI step exporting it once is consumed by all
#: three.
EnvBaseURL = "TM_BASE_URL"

#: Env-var name for the API key. Same cross-tool convention.
EnvAPIKey = "TM_API_KEY"


class Client:
    """Public TrafficMorph SDK client.

    Construct with the API key; everything else is optional:

    :param api_key: The full ``tm_…`` value provisioned from the
        in-app Settings page. Empty string is rejected because it's
        almost certainly a forgotten env-var.
    :param base_url: API base URL. Resolution order:
        ``base_url`` arg → ``$TM_BASE_URL`` env → :data:`DEFAULT_BASE_URL`.
        Passing ``base_url=""`` (explicit empty string) is rejected
        — almost certainly a misconfigured CI variable. Pass
        ``None`` (or omit the kwarg) to fall back to env / default.
        Both spellings (with and without trailing slash) work — the
        SDK normalizes to a trailing-slash form so path-prefixed
        deployments behind reverse proxies (``https://host/proxy/``)
        keep their prefix during URL resolution.
    :param timeout: Per-call timeout in seconds. Applied via
        ``httpx.Timeout`` on every request; the generator's
        endpoint functions raise ``httpx.TimeoutException`` when
        exceeded.
    :param user_agent: Override the User-Agent header (default
        :data:`DEFAULT_USER_AGENT`). Set to tag app traffic in
        TrafficMorph's server logs, e.g.
        ``"my-app/1.2.3 (tm-python-sdk/v1)"``.
    :param httpx_args: Extra kwargs forwarded verbatim to the
        underlying ``httpx.Client`` — proxies, mTLS verify
        settings, custom transports, etc.

    Access endpoints via the typed ``.api`` attribute, which is the
    generated ``AuthenticatedClient`` ready for use with the
    function-style endpoint modules::

        import json
        from trafficmorph import Client
        from trafficmorph.api.profiles import list_profiles

        c = Client(api_key="tm_...")
        resp = list_profiles.sync_detailed(client=c.api)
        if resp.status_code == 200:
            # NOTE: resp.parsed is currently None for every 2xx
            # response — the server's @ApiResponse annotations don't
            # declare body schemas yet, so openapi-python-client
            # can't auto-decode. Decode resp.content with json.loads
            # for now. The wire contract is documented in the
            # OpenAPI spec; a future SDK release will gain typed
            # responses when the spec adds response schemas.
            for profile in json.loads(resp.content):
                print(profile["id"], profile["name"])
    """

    def __init__(
        self,
        api_key: str,
        *,
        base_url: str | None = None,
        timeout: float = DEFAULT_TIMEOUT,
        user_agent: str = DEFAULT_USER_AGENT,
        httpx_args: dict[str, Any] | None = None,
    ) -> None:
        if not api_key:
            raise ValueError(
                "api_key must not be empty — provision a key from the in-app Settings page"
            )
        if not user_agent:
            raise ValueError("user_agent must not be empty")
        if timeout <= 0:
            raise ValueError(f"timeout must be positive (got {timeout!r})")

        resolved_base = _resolve_base_url(base_url)

        # X-Api-Key (not Authorization: Bearer) for the same reason
        # the CLI and Go SDK use it: easier to disambiguate from
        # JWT / OAuth flows in access-log inspection. The server
        # accepts both — see the OpenAPI spec's two security schemes.
        # Setting prefix="" makes the generator emit just the token,
        # without the default "Bearer " prefix.
        self._client = _AuthenticatedClient(
            base_url=resolved_base,
            token=api_key,
            auth_header_name="X-Api-Key",
            prefix="",
            headers={"User-Agent": user_agent},
            timeout=httpx.Timeout(timeout),
            httpx_args=(httpx_args or {}),
        )
        self._base_url = resolved_base
        self._timeout = timeout
        self._user_agent = user_agent

    @property
    def api(self) -> _AuthenticatedClient:
        """The generated client, ready to pass as ``client=`` to
        any endpoint function in :mod:`trafficmorph.api`."""
        return self._client

    @property
    def base_url(self) -> str:
        """Resolved base URL after env / option / default merge.
        Useful for diagnostics and tests."""
        return self._base_url

    @property
    def timeout(self) -> float:
        """Per-call timeout in seconds."""
        return self._timeout

    @property
    def user_agent(self) -> str:
        """The configured User-Agent header value."""
        return self._user_agent

    def __repr__(self) -> str:
        # Don't leak the API key in repr — first-rule-of-secrets.
        return (
            f"Client(base_url={self._base_url!r}, "
            f"timeout={self._timeout!r}, "
            f"user_agent={self._user_agent!r})"
        )


def _resolve_base_url(explicit: str | None) -> str:
    """Walk the precedence chain
    ``explicit → $TM_BASE_URL → DEFAULT_BASE_URL`` and normalize
    with a trailing slash.

    Argument semantics: ``explicit=None`` means "fall back to env /
    default", while ``explicit=""`` is treated as a caller mistake
    — passing an empty string clearly INTENDED to set the base URL
    but supplied nothing. Returning the default in that case silently
    routes traffic at the SaaS instance instead of the intended
    self-hosted / staging endpoint, which is exactly the kind of
    misconfiguration first-rule-of-secrets says we should
    surface, not paper over.

    Env var path: an empty ``$TM_BASE_URL`` is treated as unset
    (shell convention — ``export TM_BASE_URL=`` is the typical way
    to clear a variable in CI scripts). Only a non-empty value
    counts.

    The trailing-slash normalization is critical for path-prefixed
    deployments. The generator's client builds endpoint URLs via
    ``urljoin(base_url, "api/v1/...")``-equivalent relative
    resolution; without a trailing slash on the base, the last
    path segment is treated as a file and any prefix gets dropped
    in resolution (``https://host/proxy`` + ``api/v1/profiles``
    becomes ``https://host/api/v1/profiles`` — prefix lost). Same
    bug class the Go SDK guards against.
    """
    if explicit is not None:
        if not explicit:
            raise ValueError(
                "base_url must not be empty — pass None (the default) "
                "to fall back to $TM_BASE_URL, or a real URL string"
            )
        return _ensure_trailing_slash(explicit)

    env = os.environ.get(EnvBaseURL)
    if env:  # empty/unset env both fall through to default
        return _ensure_trailing_slash(env)

    return _ensure_trailing_slash(DEFAULT_BASE_URL)


def _ensure_trailing_slash(url: str) -> str:
    """Normalize a base URL for the generator's relative-URL
    resolution. Same helper-shape as the Go SDK's ensureTrailingSlash."""
    if url.endswith("/"):
        return url
    return url + "/"
