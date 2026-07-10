"""Run-time materialization actions used by doit link tasks.

These wrap the shared, portable ``materialize`` helper so run-time linking uses
the same safe, non-aliasing, cross-filesystem behavior as rig-time linking. The
project's configured mode (copy by default) is resolved at call time.
"""

from pdpp.utils.materialize import materialize
from pdpp.utils.project_config import get_materialize_mode


def file_linker(link_start: str, link_end: str) -> None:
    materialize(link_start, link_end, get_materialize_mode())


def dir_linker(link_start: str, link_end: str) -> None:
    materialize(link_start, link_end, get_materialize_mode())
