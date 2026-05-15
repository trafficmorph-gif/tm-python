# Python SDK build / regen / test targets.
#
#   make install        install runtime + dev deps into .venv
#   make test           run pytest in .venv
#   make regen-client   regenerate trafficmorph/ from ../cli/openapi/v1.json
#   make build          build wheel + sdist via hatchling
#   make clean          remove venvs and build artifacts
#
# Two venvs are used:
#   .venv-tools  — openapi-python-client (codegen tool only)
#   .venv        — runtime + test deps for this package
#
# Keeping them separate means the tool venv doesn't pollute the
# package's import surface (and vice versa), and a `make clean`
# wipe of one doesn't take the other down with it.

# openapi-python-client version pinned here — bumping unlocks new
# generator features but may change emitted code (and require
# updating the wrapper / tests). Treat as a deliberate upgrade
# rather than a free hop.
OAPI_CLIENT_VERSION = 0.28.4

# Source of truth for the spec is the CLI's snapshot. Same as the
# Go SDK's regen — one snapshot, three consumers. See the
# OpenApiSpecSnapshotTest Javadoc for why JSON (not YAML) is the
# canonical input.
SPEC = ../cli/openapi/v1.json

VENV_TOOLS := .venv-tools
VENV_RUN := .venv
PYTHON ?= python3

.PHONY: install test regen-client build clean tools-venv

$(VENV_TOOLS)/bin/openapi-python-client:
	$(PYTHON) -m venv $(VENV_TOOLS)
	$(VENV_TOOLS)/bin/pip install --quiet --upgrade pip
	$(VENV_TOOLS)/bin/pip install --quiet openapi-python-client==$(OAPI_CLIENT_VERSION)

tools-venv: $(VENV_TOOLS)/bin/openapi-python-client

$(VENV_RUN)/bin/pytest:
	$(PYTHON) -m venv $(VENV_RUN)
	$(VENV_RUN)/bin/pip install --quiet --upgrade pip
	# `pip install -e .[dev]` installs the package + dev extras
	# in editable mode so test changes don't need a rebuild.
	$(VENV_RUN)/bin/pip install --quiet -e ".[dev]"

install: $(VENV_RUN)/bin/pytest

test: install
	$(VENV_RUN)/bin/pytest

regen-client: tools-venv
	# --meta=none drops the generator's pyproject.toml + README +
	# scaffolding (we already have those at the sdk-python/ root).
	# The generator emits just the code (client + api/ + models/)
	# into trafficmorph/ — its native layout.
	#
	# Regen-safety: openapi-python-client's relative imports
	# (e.g. ``from ...client import AuthenticatedClient`` inside
	# api/profiles/list_profiles.py) require the generated tree
	# to live directly under the package root, NOT under a
	# sub-directory like trafficmorph/_gen/. Aliasing via
	# sys.modules breaks those relative imports. So the generator
	# owns trafficmorph/ outright; the hand-written wrapper lives
	# at trafficmorph/sdk.py (which the generator never touches),
	# and the post-step below patches the generator's __init__.py
	# to re-export the wrapper's Client.
	$(VENV_TOOLS)/bin/openapi-python-client generate \
		--path $(SPEC) \
		--config openapi/codegen-config.yaml \
		--meta=none \
		--overwrite \
		--output-path trafficmorph
	# Post-step: install / refresh the wrapper-managed block in
	# trafficmorph/__init__.py. The block contains two pieces of
	# plumbing the generator's native __init__.py doesn't include:
	#   1. `from . import api, errors, models, types` — preloads
	#      sub-packages so `import trafficmorph; trafficmorph.api`
	#      works via attribute access, not just via explicit
	#      `import trafficmorph.api`. README documents the
	#      attribute-style usage.
	#   2. `from .sdk import Client, …` — shadows the generator's
	#      Client with our wrapper AND surfaces the wrapper's
	#      module-level public constants (SPEC_VERSION,
	#      DEFAULT_BASE_URL, etc.).
	# AuthenticatedClient (the generator's authenticated client) is
	# preserved for power users via `from trafficmorph import
	# AuthenticatedClient` — exposed by the generator's native
	# __init__.py; we don't shadow it.
	#
	# Strategy: delete any existing TM-WRAPPER-BLOCK-v1 (matched
	# by sentinel markers) THEN append a fresh canonical block.
	# This is more robust than the earlier "grep && skip" guard:
	#   * Partial edits inside the block self-repair — the delete
	#     wipes whatever state was there and reinstalls.
	#   * Idempotent on any input state — block present, missing,
	#     partially-edited, or duplicated all converge to one
	#     canonical block.
	#   * Bumping the block contents is a coupled edit (this
	#     heredoc AND the matching markers in __init__.py); bump
	#     the version suffix (`-v1` → `-v2`) so a reviewer can
	#     spot the pair at a glance.
	#
	# Why sed via tempfile instead of `sed -i`: BSD sed (macOS)
	# requires `sed -i ''` while GNU sed (Linux) takes `sed -i`
	# without the empty-string arg. Tempfile round-trip works on
	# both with no further branching.
	#
	# Why a separate _wrapper_init_block.py.in file instead of an
	# inline heredoc: Make recipes treat each tab-indented line as
	# a separate shell invocation, so heredocs need .ONESHELL or
	# backslash continuation gymnastics. A `cat` of an external
	# file is one command, version-controlled, and trivially
	# editable without touching this Makefile.
	@sed '/=== TM-WRAPPER-BLOCK-v1 ===/,/=== END TM-WRAPPER-BLOCK-v1 ===/d' \
		trafficmorph/__init__.py > trafficmorph/__init__.py.tmp
	@mv trafficmorph/__init__.py.tmp trafficmorph/__init__.py
	@cat _wrapper_init_block.py.in >> trafficmorph/__init__.py

build: install
	$(VENV_RUN)/bin/pip install --quiet build
	$(VENV_RUN)/bin/python -m build

clean:
	rm -rf $(VENV_TOOLS) $(VENV_RUN) dist build *.egg-info
