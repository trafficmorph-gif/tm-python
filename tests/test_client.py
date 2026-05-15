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
    DEFAULT_BASE_URL,
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
            Client(api_key="")

    def test_rejects_empty_user_agent(self) -> None:
        with pytest.raises(ValueError, match="user_agent"):
            Client(api_key="tm_test", user_agent="")

    def test_rejects_zero_timeout(self) -> None:
        with pytest.raises(ValueError, match="timeout"):
            Client(api_key="tm_test", timeout=0)

    def test_rejects_negative_timeout(self) -> None:
        with pytest.raises(ValueError, match="timeout"):
            Client(api_key="tm_test", timeout=-1.0)

    def test_rejects_explicit_empty_base_url(self) -> None:
        """``base_url=""`` is clearly intentional but supplied
        nothing — failing fast prevents silently routing traffic
        at the SaaS default when a self-hosted deployment was
        intended. ``base_url=None`` (or omitting the kwarg) is
        the canonical "use env / default" signal."""
        with pytest.raises(ValueError, match="base_url"):
            Client(api_key="tm_test", base_url="")


# ── Base-URL resolution ──────────────────────────────────────────


class TestBaseURLResolution:
    """Same precedence chain the CLI + Go SDK use: explicit arg →
    env var → built-in default. Plus trailing-slash normalization
    for path-prefixed reverse-proxy deployments."""

    def test_default_when_nothing_set(self, monkeypatch: pytest.MonkeyPatch) -> None:
        monkeypatch.delenv(EnvBaseURL, raising=False)
        c = Client(api_key="tm_test")
        # Default is normalized — the constant itself ends with `.com`,
        # the constructor's _resolve_base_url adds the slash.
        assert c.base_url == DEFAULT_BASE_URL + "/"

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
        ],
    )
    def test_trailing_slash_normalization(self, raw: str, want: str) -> None:
        c = Client(api_key="tm_test", base_url=raw)
        assert c.base_url == want


# ── Wire-level: auth header + path prefix preserved ──────────────


def _mock_client(api_key: str, base_url: str, response_handler) -> Client:
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
        Without proper trailing-slash handling in
        :func:`_resolve_base_url`, ``https://host/proxy-prefix`` +
        relative ``api/v1/profiles`` would resolve to
        ``https://host/api/v1/profiles`` — the prefix gets dropped.
        """
        seen_paths: list[str] = []

        def handler(req: httpx.Request) -> httpx.Response:
            seen_paths.append(req.url.path)
            return httpx.Response(200, json=[])

        # Run the same request twice — once with prefix-no-slash,
        # once with prefix-trailing-slash — and assert both wire
        # paths look identical and carry the prefix.
        for base in ["https://example.com/proxy-prefix", "https://example.com/proxy-prefix/"]:
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
    c = Client(api_key="tm_secret_should_not_appear_here", base_url="https://example.com")
    r = repr(c)
    assert "tm_secret_should_not_appear_here" not in r
    assert "base_url" in r  # but it should still be informative


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

    This test catches the post-step omission: it imports
    ``trafficmorph.Client`` and asserts it's the wrapper class
    (defined in trafficmorph.sdk).
    """
    import trafficmorph
    import trafficmorph.sdk as wrapper_module
    import trafficmorph.client as generator_module

    assert trafficmorph.Client is wrapper_module.Client, (
        "trafficmorph.Client must be the wrapper from trafficmorph.sdk. "
        "If this fails, the Makefile regen-client target's post-step "
        "didn't run (it appends `from .sdk import Client` to __init__.py "
        "after the generator overwrites it). Re-run `make regen-client`."
    )
    assert trafficmorph.Client is not generator_module.Client, (
        "trafficmorph.Client must shadow the generator's unauthenticated "
        "Client — same name, different class."
    )


def test_subpackages_accessible_via_attribute_after_bare_import() -> None:
    """README emphasizes ``trafficmorph.api.<tag>`` module access.
    Users who reach for that path via attribute navigation
    (``import trafficmorph; trafficmorph.api.profiles…``) hit
    AttributeError unless the package __init__ explicitly preloads
    the sub-packages. The generator's native __init__.py doesn't —
    the wrapper layer DOES, via a ``from . import api, errors,
    models, types`` line. Lock the behavior in so the Makefile's
    regen-client post-step (which has to re-apply this line)
    doesn't silently regress."""
    # Use importlib to bypass any module-level caching from earlier
    # test runs that did `import trafficmorph.api` and registered
    # the sub-module in sys.modules.
    import importlib
    import sys

    # Drop any cached trafficmorph.* entries so the next import
    # exercises the fresh __init__.py path.
    for name in list(sys.modules):
        if name == "trafficmorph" or name.startswith("trafficmorph."):
            del sys.modules[name]

    tm = importlib.import_module("trafficmorph")
    # All four sub-packages must be bound as attributes WITHOUT a
    # separate `import trafficmorph.api` line.
    for sub in ("api", "errors", "models", "types"):
        assert hasattr(tm, sub), (
            f"trafficmorph.{sub} not accessible via attribute — the "
            f"__init__.py is missing the `from . import api, errors, "
            f"models, types` preload. If you're seeing this fail "
            f"after a regen, re-run `make regen-client` (the post-step "
            f"re-applies the preload)."
        )


def test_endpoint_imports_use_canonical_paths() -> None:
    """Confirms the README's claim that
    ``from trafficmorph.api.profiles import list_profiles`` works.
    With the generator owning trafficmorph/ outright, this just
    exercises the generator's native layout — no aliasing magic.
    Test exists to guard against future refactors that try to
    relocate the generated code (any such relocation would have
    to either preserve relative imports or rewrite them)."""
    from trafficmorph.api.profiles import list_profiles
    from trafficmorph.api.runs import start
    from trafficmorph.api.history import get_history_item

    for endpoint in (list_profiles, start, get_history_item):
        assert callable(endpoint.sync_detailed)
        assert callable(endpoint.asyncio_detailed)
