"""Portable, non-destructive file materialization for pdpp.

pdpp copies each task's declared dependency files from an upstream task's
``output/`` directory into this task's ``input/`` directory. Historically it
did this with bare ``os.link`` (hard links), which has three hazards:

- editing a linked ``input/`` file in place silently rewrote the authoritative
  upstream ``output/`` file, because both names pointed at the same inode;
- a hard link cannot span filesystems (``EXDEV``) and fails on Windows
  FAT/exFAT and most network drives, with no fallback; and
- the rig-time linker wiped the whole ``input/`` directory first, deleting any
  file a user had placed there manually.

This module provides a single ``materialize`` entry point used by both the
rig-time and run-time paths. The default mode is ``copy``, which is safe on
every filesystem and never aliases upstream outputs. ``hardlink`` and
``symlink`` modes remain available for users who want them; both fall back to a
copy when the target filesystem cannot support the requested link type.
"""

import os
import shutil
from typing import Literal

MaterializeMode = Literal["copy", "hardlink", "symlink"]

VALID_MODES = ("copy", "hardlink", "symlink")
DEFAULT_MODE: MaterializeMode = "copy"


def _copy_path(src: str, dst: str) -> None:
    if os.path.isdir(src):
        shutil.copytree(src, dst)
    else:
        shutil.copy2(src, dst)


def _hardlink_path(src: str, dst: str) -> None:
    if os.path.isdir(src):
        shutil.copytree(src, dst, copy_function=os.link)
    else:
        os.link(src, dst)


def _symlink_path(src: str, dst: str) -> None:
    os.symlink(os.path.abspath(src), dst)


def materialize(src: str, dst: str, mode: MaterializeMode = DEFAULT_MODE) -> str:
    """Materialize ``src`` at ``dst`` using ``mode``.

    Overwrites an existing ``dst`` (removing it first so a stale hard link or
    symlink cannot leave the old inode in place). On ``EXDEV`` or any
    ``OSError`` from a link operation (cross-filesystem, unsupported Windows
    drive), falls back to a copy so materialization never crashes.

    Returns the mode actually used (``"copy"`` when a link fell back).
    """
    if mode not in VALID_MODES:
        raise ValueError(f"Unknown materialization mode: {mode!r}")

    if os.path.lexists(dst):
        if os.path.isdir(dst) and not os.path.islink(dst):
            shutil.rmtree(dst)
        else:
            os.remove(dst)

    if mode == "copy":
        _copy_path(src, dst)
        return "copy"

    linker = _hardlink_path if mode == "hardlink" else _symlink_path
    try:
        linker(src, dst)
        return mode
    except OSError:
        # Cross-filesystem (EXDEV), unsupported drive, or platform limitation.
        if os.path.lexists(dst):
            if os.path.isdir(dst) and not os.path.islink(dst):
                shutil.rmtree(dst)
            else:
                os.remove(dst)
        _copy_path(src, dst)
        return "copy"
