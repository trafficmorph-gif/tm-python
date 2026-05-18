
""" A client library for accessing TrafficMorph API """
from .client import AuthenticatedClient, Client

__all__ = (
    "AuthenticatedClient",
    "Client",
)

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
