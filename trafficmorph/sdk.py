"""TrafficMorph Python SDK — ergonomic public surface.

This module defines :class:`Client`, the public entry point. The
sibling modules under ``trafficmorph/`` (client.py, errors.py,
types.py, api/, models/) hold the typed request / response classes
and endpoint functions :class:`Client` exposes via the ``.api``
attribute.

The public surface is re-exported through ``trafficmorph.__init__``
so callers do::

    from trafficmorph import Client
    from trafficmorph.api.profiles import list_profiles

without needing to import this module directly.
"""

from __future__ import annotations

import os
from typing import Any
from urllib.parse import urlsplit, urlunsplit

import httpx

# Generator's ``AuthenticatedClient`` is the workhorse — httpx-based
# attrs class that we hand to the generated endpoint functions via
# the ``client=`` kwarg. Importing it under an underscore name keeps
# our public surface unambiguous: ``Client`` (defined below) is OUR
# wrapper, the generator's class is an implementation detail.
from .client import AuthenticatedClient as _AuthenticatedClient

__all__ = (
    "Client",
    "SPEC_VERSION",
    "DEFAULT_USER_AGENT",
    "DEFAULT_TIMEOUT",
    "EnvBaseURL",
    "EnvAPIKey",
)

#: Which ``/api/v1`` revision this build targets.
SPEC_VERSION = "v1"

#: Default User-Agent sent on every request when the caller doesn't
#: override via ``user_agent=``. Includes the SDK name and the API
#: version so server-side observability can correlate client
#: revisions to API surface revisions.
DEFAULT_USER_AGENT = f"tm-python-sdk/{SPEC_VERSION}"

#: Default per-call HTTP timeout in seconds. Generous enough for
#: the heaviest v1 endpoint on a slow-network laptop; callers
#: running latency-sensitive automation should override.
DEFAULT_TIMEOUT = 30.0

#: Env-var name for the API base URL. Same convention as the
#: ``tm`` CLI and the Go SDK so one ``export`` works for all.
EnvBaseURL = "TM_BASE_URL"

#: Env-var name for the API key. Same cross-tool convention.
EnvAPIKey = "TM_API_KEY"


class Client:
    """Public TrafficMorph SDK client.

    :param api_key: The full ``tm_…`` value provisioned from the
        in-app Settings page. Empty string is rejected because
        it's almost certainly a forgotten env-var. Rejected too if
        it contains any byte that httpx would refuse to send as a
        header value — ASCII controls 0x00–0x1F (except HTAB) and
        DEL (0x7F).
    :param base_url: API base URL. Required — pass via this kwarg
        OR set ``$TM_BASE_URL`` before construction. There is no
        built-in default. Either spelling (with or without
        trailing slash) works; the SDK normalizes to a trailing-
        slash form so path-prefixed deployments behind reverse
        proxies (``https://host/proxy/``) keep their prefix during
        URL resolution. Malformed values (missing scheme, wrong
        scheme, no host, query string, fragment) are rejected at
        construction time rather than failing late inside httpx.
        Percent-encoded path segments are preserved verbatim:
        ``/a%2Fb`` stays ``/a%2Fb``, not ``/a/b`` (per RFC 3986
        these are semantically different paths).
    :param timeout: Per-call timeout in seconds. Applied via
        ``httpx.Timeout`` on every request; the generator's
        endpoint functions raise ``httpx.TimeoutException`` when
        exceeded.
    :param user_agent: Override the User-Agent header (default
        :data:`DEFAULT_USER_AGENT`). Subject to the same header-
        byte validation as ``api_key``.
    :param httpx_args: Extra kwargs forwarded verbatim to the
        underlying ``httpx.Client`` — proxies, mTLS verify
        settings, custom transports, etc.

    Access endpoints via the typed ``.api`` attribute, which is
    the generator's ``AuthenticatedClient`` ready for use with
    the function-style endpoint modules::

        import json
        from trafficmorph import Client
        from trafficmorph.api.profiles import list_profiles

        c = Client(api_key="tm_...", base_url="http://localhost:8080")
        resp = list_profiles.sync_detailed(client=c.api)
        if resp.status_code == 200:
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
        _check_header_value("api_key", api_key)

        if not user_agent:
            raise ValueError("user_agent must not be empty")
        _check_header_value("user_agent", user_agent)

        if timeout <= 0:
            raise ValueError(f"timeout must be positive (got {timeout!r})")

        resolved_base = _resolve_base_url(base_url)

        # X-Api-Key (not Authorization: Bearer); the API accepts both.
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
        """The generator's client, ready to pass as ``client=``
        to any endpoint function in :mod:`trafficmorph.api`."""
        return self._client

    @property
    def base_url(self) -> str:
        """Resolved base URL after env / arg / normalize. Useful
        for diagnostics and tests."""
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


# ── Base-URL pipeline ────────────────────────────────────────────


def _resolve_base_url(explicit: str | None) -> str:
    """Resolve the base URL from kwarg + env, validate it, and
    return the normalized form. Single pipeline so both sources
    produce identical results for the same logical input.

    Argument semantics:

    * ``explicit=None`` (or omitted): fall back to ``$TM_BASE_URL``.
      If the env var is also unset, raise — there is NO built-in
      default. Callers must point the SDK at a real TrafficMorph
      install (``http://localhost:8080`` for local dev, your hosted
      URL otherwise).
    * ``explicit=""``: rejected as a likely caller mistake (a
      misconfigured CI variable that resolved to empty string).
      Pass ``None`` to opt into env fallback.
    * Any non-empty string: validated and normalized.

    Validation rejects malformed URLs upfront with a clear error,
    rather than letting them fail late inside httpx with an opaque
    transport-layer message.
    """
    if explicit is not None and explicit == "":
        raise ValueError(
            "base_url must not be empty — pass None (the default) to "
            "fall back to $TM_BASE_URL, or supply a real URL string"
        )

    raw: str | None
    source_label: str
    if explicit is not None:
        raw = explicit
        source_label = "base_url"
    else:
        env_value = os.environ.get(EnvBaseURL, "")
        if not env_value.strip():
            raise ValueError(
                f"base_url is required: pass base_url='http://…' to Client(...) "
                f"or set ${EnvBaseURL} before constructing the client"
            )
        raw = env_value
        source_label = f"${EnvBaseURL}"

    try:
        _validate_base_url(raw)
    except ValueError as e:
        raise ValueError(f"{source_label}: {e}") from None

    return _normalize_base_url(raw)


def _validate_base_url(raw: str) -> None:
    """Raise ``ValueError`` if ``raw`` is not an absolute http/https
    URL with a non-empty host and no query/fragment.

    Catches the common malformed-input cases that would otherwise
    fail late on the first API call (or worse — silently misroute):

    * ``""`` or whitespace-only            → "must not be empty"
    * ``"localhost:8080"`` (no scheme)     → "must include … scheme"
    * ``"ftp://x"`` (wrong scheme)         → "must be http or https"
    * ``"https://"`` (no host)             → "must include a host"
    * ``"https://x/?q=1"`` (query)         → "must not contain a query string"
    * ``"https://x/#frag"`` (fragment)     → "must not contain a fragment"

    Query strings and fragments are rejected because they corrupt
    routing semantics: a base URL is the deployment root, not a
    per-request URL. Per-request params should attach at the
    endpoint call site.

    The string is trimmed before parsing; surrounding whitespace
    is almost always a copy-paste artifact.
    """
    raw = raw.strip()
    if not raw:
        raise ValueError("base URL must not be empty")

    parts = urlsplit(raw)

    if not parts.scheme:
        raise ValueError(
            f"base URL {raw!r} must include http:// or https:// scheme "
            f"(got no scheme — did you mean http://{raw}?)"
        )
    if parts.scheme not in ("http", "https"):
        raise ValueError(
            f"base URL {raw!r} has scheme {parts.scheme!r}; must be http or https"
        )
    if not parts.netloc:
        raise ValueError(f"base URL {raw!r} must include a host")
    if parts.query:
        raise ValueError(
            f"base URL {raw!r} must not contain a query string "
            f"(have {parts.query!r}); attach per-request params at the "
            f"endpoint call site instead"
        )
    if parts.fragment:
        raise ValueError(
            f"base URL {raw!r} must not contain a fragment "
            f"(have {parts.fragment!r}); fragments are client-side only "
            f"and have no meaning to the server"
        )


def _normalize_base_url(raw: str) -> str:
    """Trim the input and append a trailing slash to the path
    component if missing. Call AFTER :func:`_validate_base_url`
    so the URL is known well-formed.

    Why structural (urlsplit/urlunsplit) instead of just appending
    ``"/"`` to the raw string: a naive append would land the slash
    on a query or fragment for inputs like ``https://x?q=1`` —
    silently producing ``https://x?q=1/``. Validation rejects
    those upstream, but doing the slash placement on the path
    component keeps the function correct even if a future code
    path bypasses validation.

    Python's ``urlsplit`` keeps the path's percent-encoding
    intact (unlike Go's net/url, which decodes into a separate
    field). That means ``%2F`` in the input survives end-to-end:
    ``/a%2Fb`` is one path segment, ``/a/b`` is two — the SDK
    never collapses one into the other.
    """
    raw = raw.strip()
    parts = urlsplit(raw)
    path = parts.path
    if not path.endswith("/"):
        path = path + "/"
    return urlunsplit(parts._replace(path=path))


# ── Header-value pipeline ────────────────────────────────────────


def _check_header_value(field_name: str, value: str) -> None:
    """Raise ``ValueError`` if ``value`` contains a byte httpx would
    refuse to send as a header value.

    Per RFC 7230 §3.2.6, a header field-value is built from VCHAR
    (0x21–0x7E), SP (0x20), HTAB (0x09), and obs-text (0x80–0xFF).
    We reject anything outside that set: ASCII controls 0x00–0x1F
    other than HTAB, and DEL (0x7F). Mirrors what httpx /
    h11 reject at request-build time — catching here means the
    caller sees a clear ``ValueError`` at ``Client(...)`` rather
    than an opaque transport error mid-call.

    CR and LF specifically would enable header-injection attacks
    (a key with embedded ``\\r\\n`` could splice in arbitrary extra
    headers); NUL would corrupt the wire encoding; DEL is rejected
    by the stdlib's RFC-7230 check. The named cases below cover
    the bytes a caller is most likely to have stumbled into; the
    fallback hex form handles the rest.
    """
    for i, ch in enumerate(value):
        code = ord(ch)
        if ch == "\t" or (0x20 <= code <= 0x7E) or code >= 0x80:
            continue
        what = _describe_control_byte(code)
        raise ValueError(
            f"{field_name}: value contains {what} at position {i}; "
            f"HTTP header values cannot contain ASCII control bytes "
            f"(per RFC 7230, only HTAB, SP, VCHAR, and obs-text are allowed)"
        )


def _describe_control_byte(code: int) -> str:
    """Friendly name for a rejected byte. Named cases for the
    values a caller is most likely to have hit; hex fallback for
    everything else."""
    if code == 0x0D:
        return "a carriage return (CR, 0x0D)"
    if code == 0x0A:
        return "a newline (LF, 0x0A)"
    if code == 0x00:
        return "a NUL byte (0x00)"
    if code == 0x7F:
        return "a DEL byte (0x7F)"
    return f"a control byte (0x{code:02X})"
