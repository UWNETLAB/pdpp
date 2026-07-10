"""Per-project pdpp configuration.

Currently the only setting is the file-materialization mode used when copying
task dependencies from an upstream ``output/`` into a downstream ``input/``.

Resolution order (first match wins):

1. the ``PDPP_MATERIALIZE_MODE`` environment variable;
2. ``[tool.pdpp] materialize_mode`` in a ``pdpp.toml`` file in the current
   working directory (the project root);
3. the safe default, ``copy``.
"""

import os
import tomllib
from pathlib import Path

from pdpp.utils.materialize import DEFAULT_MODE, VALID_MODES, MaterializeMode

PROJECT_CONFIG_FILENAME = "pdpp.toml"
_ENV_VAR = "PDPP_MATERIALIZE_MODE"


def _validated(mode: str, source: str) -> MaterializeMode:
    if mode not in VALID_MODES:
        raise ValueError(
            f"Invalid materialize mode {mode!r} from {source}; "
            f"expected one of {', '.join(VALID_MODES)}."
        )
    return mode  # type: ignore[return-value]


def get_materialize_mode() -> MaterializeMode:
    """Resolve the materialization mode for the current project."""
    env_mode = os.environ.get(_ENV_VAR)
    if env_mode:
        return _validated(env_mode.strip().lower(), _ENV_VAR)

    config_path = Path(PROJECT_CONFIG_FILENAME)
    if config_path.is_file():
        with config_path.open("rb") as stream:
            data = tomllib.load(stream)
        mode = data.get("tool", {}).get("pdpp", {}).get("materialize_mode")
        if mode is not None:
            return _validated(str(mode).strip().lower(), str(config_path))

    return DEFAULT_MODE
