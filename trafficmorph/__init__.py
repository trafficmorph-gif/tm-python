"""TrafficMorph Python SDK.

This file is the generator's native ``__init__.py`` PLUS a single
re-export of the public ``Client`` wrapper from
:mod:`trafficmorph.sdk`. The Makefile's ``regen-client`` target
re-applies the re-export line after every generator run so the
wrapper stays exposed across regenerations.

Most callers want :class:`trafficmorph.Client` (the wrapper) — it
handles auth, env-var resolution, and base-URL normalization.
The generator's unauthenticated ``Client`` is still reachable as
``trafficmorph.client.Client`` for power users.

See ``sdk-python/README.md`` for the layout rationale: the
generator emits everything under ``trafficmorph/`` directly,
which means hand-written code can't share that directory without
getting clobbered on regen. The wrapper lives at
``trafficmorph/sdk.py`` and the re-export at the bottom of this
file is the regen-stable bridge between the two.
"""
from .client import AuthenticatedClient, Client as _GeneratedClient



# === TM-WRAPPER-BLOCK-v1 === (managed by Makefile regen-client; do not hand-edit)
from . import api, errors, models, types  # noqa: F401
from .sdk import (  # noqa: E402, F401
    Client,
    SPEC_VERSION,
    DEFAULT_BASE_URL,
    DEFAULT_USER_AGENT,
    DEFAULT_TIMEOUT,
    EnvBaseURL,
    EnvAPIKey,
)

__all__ = (
    "Client",
    "AuthenticatedClient",
    "SPEC_VERSION",
    "DEFAULT_BASE_URL",
    "DEFAULT_USER_AGENT",
    "DEFAULT_TIMEOUT",
    "EnvBaseURL",
    "EnvAPIKey",
)
# === END TM-WRAPPER-BLOCK-v1 ===
