"""Unit tests for the trafficmorph public Client wrapper.

The Go SDK's test suite ships an httpx-test-server hooked up to a
real endpoint call. The Python SDK does the equivalent via
``httpx.MockTransport`` — same wire-level contract, just routed
through the test transport instead of a real socket. That's the
only way to verify the auth header and base-URL normalization
actually reach the wire.
"""

from __future__ import annotations

import httpx
import pytest

from trafficmorph import (
    DEFAULT_USER_AGENT,
    EnvBaseURL,
    SPEC_VERSION,
    Client,
)
from trafficmorph.api.profiles import list_profiles


# ── Constructor validation ────────────────────────────────────────


class TestConstructorValidation:
    """Caller-side mistakes must surface at construction, not later
    via an opaque httpx error mid-call."""

    def test_rejects_empty_api_key(self) -> None:
        with pytest.raises(ValueError, match="api_key"):
            Client(api_key="", base_url="https://example.com")

    def test_rejects_empty_user_agent(self) -> None:
        with pytest.raises(ValueError, match="user_agent"):
            Client(api_key="tm_test", base_url="https://example.com", user_agent="")

    def test_rejects_zero_timeout(self) -> None:
        with pytest.raises(ValueError, match="timeout"):
            Client(api_key="tm_test", base_url="https://example.com", timeout=0)

    def test_rejects_negative_timeout(self) -> None:
        with pytest.raises(ValueError, match="timeout"):
            Client(api_key="tm_test", base_url="https://example.com", timeout=-1.0)

    def test_rejects_explicit_empty_base_url(self) -> None:
        """``base_url=""`` is clearly intentional but supplied
        nothing — failing fast prevents silent misconfiguration.
        ``base_url=None`` (or omitting the kwarg) is the canonical
        "use env" signal."""
        with pytest.raises(ValueError, match="base_url"):
            Client(api_key="tm_test", base_url="")


# ── Base-URL: required, no built-in default ──────────────────────


class TestBaseURLRequired:
    """No built-in default — the SDK used to fall back to a
    placeholder example.com host that doesn't resolve. Now any
    caller missing both the kwarg AND the env var hits a clear
    constructor error."""

    def test_missing_both_kwarg_and_env_errors(
        self, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        monkeypatch.delenv(EnvBaseURL, raising=False)
        with pytest.raises(ValueError) as excinfo:
            Client(api_key="tm_test")
        msg = str(excinfo.value)
        assert "base_url is required" in msg
        assert EnvBaseURL in msg, "error should name the env var as a recovery path"


# ── Base-URL resolution + normalization ───────────────────────────


class TestBaseURLResolution:
    """Same precedence chain the CLI + Go SDK use: explicit arg →
    env var. Plus trailing-slash normalization for path-prefixed
    reverse-proxy deployments."""

    def test_env_var_when_no_arg(self, monkeypatch: pytest.MonkeyPatch) -> None:
        monkeypatch.setenv(EnvBaseURL, "https://staging.example.com")
        c = Client(api_key="tm_test")
        assert c.base_url == "https://staging.example.com/"

    def test_explicit_arg_overrides_env(self, monkeypatch: pytest.MonkeyPatch) -> None:
        monkeypatch.setenv(EnvBaseURL, "https://env-says.example.com")
        c = Client(api_key="tm_test", base_url="https://flag-says.example.com")
        assert c.base_url == "https://flag-says.example.com/"

    @pytest.mark.parametrize(
        "raw, want",
        [
            ("https://example.com", "https://example.com/"),
            ("https://example.com/", "https://example.com/"),
            ("https://example.com/prefix", "https://example.com/prefix/"),
            ("https://example.com/prefix/", "https://example.com/prefix/"),
            # Multi-segment prefix — common in nested reverse-proxy mounts.
            ("https://host/team/app", "https://host/team/app/"),
            # Surrounding whitespace tolerated (copy-paste artifact).
            ("  https://example.com  ", "https://example.com/"),
        ],
    )
    def test_trailing_slash_normalization(self, raw: str, want: str) -> None:
        c = Client(api_key="tm_test", base_url=raw)
        assert c.base_url == want


# ── Base-URL: malformed inputs rejected upfront ──────────────────


class TestBaseURLMalformedInputs:
    """Bad inputs that would otherwise fail late inside httpx
    (or worse — silently misroute) get caught at construction."""

    @pytest.mark.parametrize(
        "bad, want_substr",
        [
            ("localhost:8080", "scheme"),
            ("ftp://example.com", "http or https"),
            ("https://", "host"),
            ("   ", "must not be empty"),
            # Query string and fragment in the base URL would corrupt
            # per-request routing — refuse outright.
            ("https://example.com/?x=1", "query"),
            ("https://example.com/team/app?x=1", "query"),
            ("https://example.com/#frag", "fragment"),
            ("https://example.com/?x=1#frag", "query"),
        ],
    )
    def test_rejects_malformed(self, bad: str, want_substr: str) -> None:
        with pytest.raises(ValueError, match=want_substr):
            Client(api_key="tm_test", base_url=bad)

    def test_env_path_uses_same_validation(
        self, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        """A bad env value must fail with the same clarity as a bad
        kwarg — and the error message should name the env var, not
        the kwarg, so the user knows where to look."""
        monkeypatch.setenv(EnvBaseURL, "localhost:8080")
        with pytest.raises(ValueError) as excinfo:
            Client(api_key="tm_test")
        msg = str(excinfo.value)
        assert EnvBaseURL in msg, f"error should name {EnvBaseURL}, got: {msg}"
        assert "scheme" in msg

    def test_env_error_preserves_input_verbatim(
        self, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        """The env-path error message must reference the value the
        user set, not a normalized variant. Earlier code pre-appended
        a slash before validating, so ``?x=1`` was reported as
        ``x=1/`` — synthetic slash the user never typed."""
        monkeypatch.setenv(EnvBaseURL, "https://example.com?x=1")
        with pytest.raises(ValueError) as excinfo:
            Client(api_key="tm_test")
        msg = str(excinfo.value)
        assert "x=1/" not in msg, (
            f"error must not contain SDK-synthesized trailing slash; got: {msg}"
        )


# ── Base-URL: %2F preservation + option/env parity ───────────────


class TestPercentEncodedPathParity:
    """``%2F`` (percent-encoded slash) and ``/`` are semantically
    DIFFERENT path segments per RFC 3986 — ``/a%2Fb`` is one
    segment containing a literal slash, ``/a/b`` is two segments.
    The SDK must preserve the encoding through validate +
    normalize, and the option path and env path must produce
    identical BaseURL output for the same logical input.
    """

    @pytest.mark.parametrize(
        "raw",
        [
            "https://example.com/a%2Fb",
            "https://example.com/team%2Fnested/app",
            "https://example.com/path%21bang",
        ],
    )
    def test_option_and_env_parity(
        self, raw: str, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        monkeypatch.delenv(EnvBaseURL, raising=False)
        c_opt = Client(api_key="tm_test", base_url=raw)

        monkeypatch.setenv(EnvBaseURL, raw)
        c_env = Client(api_key="tm_test")

        assert c_opt.base_url == c_env.base_url, (
            f"parity violated for {raw!r}: option={c_opt.base_url!r} "
            f"env={c_env.base_url!r}"
        )

    def test_percent_2f_not_decoded(self) -> None:
        """The encoded slash must survive into the stored base URL.
        If we ever silently decoded ``%2F`` into ``/``, the path
        segment count changes — a 1-segment path becomes 2-segment
        and routing breaks."""
        c = Client(api_key="tm_test", base_url="https://example.com/a%2Fb")
        assert c.base_url == "https://example.com/a%2Fb/", (
            f"%2F got decoded into literal /: {c.base_url}"
        )


# ── Header-byte validation (api_key + user_agent) ────────────────


class TestHeaderByteValidation:
    """httpx rejects ASCII controls 0x00-0x1F (except HTAB) and
    DEL (0x7F) in header values, but its check fires deep inside
    request construction. Catching upfront at ``Client(...)`` gives
    a clear error pointing at the bad input."""

    @pytest.mark.parametrize(
        "bad_key, name_or_hex",
        [
            ("tm_x\rmore", "carriage return"),
            ("tm_x\nInjected: yes", "newline"),
            ("tm_x\x00", "NUL"),
            ("tm_x\r\nX-Injected: yes", "carriage return"),
            # The broader rule beyond CR/LF/NUL — any byte httpx
            # would refuse.
            ("tm_x\x01", "0x01"),
            ("tm_x\x1bmore", "0x1B"),
            ("tm_x\x7f", "DEL"),
        ],
    )
    def test_rejects_invalid_chars_in_api_key(
        self, bad_key: str, name_or_hex: str
    ) -> None:
        with pytest.raises(ValueError) as excinfo:
            Client(api_key=bad_key, base_url="https://example.com")
        msg = str(excinfo.value)
        assert "api_key" in msg
        assert name_or_hex in msg, (
            f"error should name the bad byte ({name_or_hex}); got: {msg}"
        )

    @pytest.mark.parametrize(
        "bad_ua, name_or_hex",
        [
            ("my-app\rfoo", "carriage return"),
            ("my-app\nfoo", "newline"),
            ("my-app\x00", "NUL"),
            ("my-app\x7f", "DEL"),
        ],
    )
    def test_rejects_invalid_chars_in_user_agent(
        self, bad_ua: str, name_or_hex: str
    ) -> None:
        with pytest.raises(ValueError) as excinfo:
            Client(
                api_key="tm_test", base_url="https://example.com", user_agent=bad_ua
            )
        msg = str(excinfo.value)
        assert "user_agent" in msg
        assert name_or_hex in msg


# ── Wire-level: auth header, UA, path prefix, %2F ────────────────


def _mock_client(
    api_key: str, base_url: str, response_handler
) -> Client:
    """Build a Client whose underlying httpx transport is a
    MockTransport that runs ``response_handler`` for every request.
    Lets tests verify the headers / path that actually reach the
    wire without standing up a real server."""
    transport = httpx.MockTransport(response_handler)
    return Client(
        api_key=api_key,
        base_url=base_url,
        httpx_args={"transport": transport},
    )


class TestWireLevelContract:
    """The wire-level proofs. Pure unit tests on properties can't
    catch these — verification must go through the actual httpx
    transport so we observe what the server would see."""

    def test_x_api_key_header_is_injected(self) -> None:
        seen: dict[str, str] = {}

        def handler(req: httpx.Request) -> httpx.Response:
            seen["api_key"] = req.headers.get("X-Api-Key", "")
            seen["auth"] = req.headers.get("Authorization", "")
            seen["ua"] = req.headers.get("User-Agent", "")
            return httpx.Response(200, json=[])

        c = _mock_client("tm_secret_xyz", "https://example.com", handler)
        resp = list_profiles.sync_detailed(client=c.api)
        assert resp.status_code == 200, resp.content
        assert seen["api_key"] == "tm_secret_xyz", "X-Api-Key header not injected"
        # X-Api-Key form deliberately omits the Authorization header.
        assert seen["auth"] == "", "must not also send Authorization: Bearer"

    def test_default_user_agent_includes_spec_version(self) -> None:
        seen: dict[str, str] = {}

        def handler(req: httpx.Request) -> httpx.Response:
            seen["ua"] = req.headers.get("User-Agent", "")
            return httpx.Response(200, json=[])

        c = _mock_client("tm_test", "https://example.com", handler)
        list_profiles.sync_detailed(client=c.api)
        assert seen["ua"].startswith("tm-python-sdk/"), seen["ua"]
        assert SPEC_VERSION in seen["ua"], seen["ua"]

    def test_custom_user_agent_overrides(self) -> None:
        seen: dict[str, str] = {}

        def handler(req: httpx.Request) -> httpx.Response:
            seen["ua"] = req.headers.get("User-Agent", "")
            return httpx.Response(200, json=[])

        transport = httpx.MockTransport(handler)
        c = Client(
            api_key="tm_test",
            base_url="https://example.com",
            user_agent="my-app/1.2.3 (tm-python-sdk/v1)",
            httpx_args={"transport": transport},
        )
        list_profiles.sync_detailed(client=c.api)
        assert seen["ua"] == "my-app/1.2.3 (tm-python-sdk/v1)"

    def test_path_prefix_is_preserved(self) -> None:
        """Regression guard for path-prefixed reverse-proxy mounts.
        Without proper trailing-slash handling, ``https://host/proxy-prefix``
        + relative ``api/v1/profiles`` would resolve to
        ``https://host/api/v1/profiles`` — the prefix gets dropped."""
        seen_paths: list[str] = []

        def handler(req: httpx.Request) -> httpx.Response:
            seen_paths.append(req.url.path)
            return httpx.Response(200, json=[])

        for base in [
            "https://example.com/proxy-prefix",
            "https://example.com/proxy-prefix/",
        ]:
            c = _mock_client("tm_test", base, handler)
            list_profiles.sync_detailed(client=c.api)

        assert len(seen_paths) == 2
        for path in seen_paths:
            assert path.startswith("/proxy-prefix/"), f"path prefix dropped: {path}"
            assert "/api/v1/profiles" in path, f"endpoint path missing: {path}"


# ── repr() doesn't leak the key ──────────────────────────────────


def test_repr_does_not_leak_api_key() -> None:
    """First-rule-of-secrets: never log an API key. The Client's
    __repr__ output ends up in tracebacks, debug logs, and exception
    messages — must not embed the secret."""
    c = Client(
        api_key="tm_secret_should_not_appear_here", base_url="https://example.com"
    )
    r = repr(c)
    assert "tm_secret_should_not_appear_here" not in r
    assert "base_url" in r  # but it should still be informative


# ── Wrapper-vs-generator identity + regen-safety ─────────────────


def test_public_client_is_the_wrapper_not_the_generator() -> None:
    """Regen-safety lock-in. The generator emits its own ``Client``
    class at ``trafficmorph.client.Client`` and re-exports it from
    ``trafficmorph/__init__.py``. Our wrapper is in
    ``trafficmorph/sdk.py`` and the Makefile's regen-client target
    appends ``from .sdk import Client`` to the generator's
    ``__init__.py`` after every regen — that shadows the
    generator's Client so ``from trafficmorph import Client``
    resolves to OUR wrapper.

    If that post-step regression-fails, ``trafficmorph.Client``
    would silently become the generator's class — same name, but
    no api_key validation, no env-var resolution, no base-URL
    normalization. CI users wouldn't notice until they ran into
    a missing-feature wall mid-flight.
    """
    import trafficmorph
    import trafficmorph.sdk as wrapper_module
    import trafficmorph.client as generator_module

    assert trafficmorph.Client is wrapper_module.Client, (
        "trafficmorph.Client must be the wrapper from trafficmorph.sdk."
    )
    assert trafficmorph.Client is not generator_module.Client


def test_subpackages_accessible_via_attribute_after_bare_import() -> None:
    """README emphasizes ``trafficmorph.api.<tag>`` module access.
    Lock in that the wrapper layer's preload of sub-packages
    survives regen (the Makefile re-applies the line)."""
    import importlib
    import sys

    for name in list(sys.modules):
        if name == "trafficmorph" or name.startswith("trafficmorph."):
            del sys.modules[name]

    tm = importlib.import_module("trafficmorph")
    for sub in ("api", "errors", "models", "types"):
        assert hasattr(tm, sub), (
            f"trafficmorph.{sub} not accessible via attribute"
        )


def test_endpoint_imports_use_canonical_paths() -> None:
    """Confirms the README's claim that
    ``from trafficmorph.api.profiles import list_profiles`` works.
    Test exists to guard against future refactors that try to
    relocate the generated code."""
    from trafficmorph.api.profiles import list_profiles
    from trafficmorph.api.runs import start
    from trafficmorph.api.history import get_history_item

    for endpoint in (list_profiles, start, get_history_item):
        assert callable(endpoint.sync_detailed)
        assert callable(endpoint.asyncio_detailed)
