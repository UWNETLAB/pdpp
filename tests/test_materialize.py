import os
from pathlib import Path

import pytest

from pdpp.utils.materialize import materialize


def test_copy_is_default_and_does_not_alias(tmp_path: Path) -> None:
    src = tmp_path / "out.csv"
    src.write_text("v1")
    dst = tmp_path / "in.csv"

    used = materialize(str(src), str(dst))

    assert used == "copy"
    assert dst.read_text() == "v1"
    # Editing the copy must NOT change the upstream source (no aliasing).
    dst.write_text("edited")
    assert src.read_text() == "v1"


def test_copy_directory(tmp_path: Path) -> None:
    src = tmp_path / "outdir"
    src.mkdir()
    (src / "a.txt").write_text("a")
    dst = tmp_path / "indir"

    materialize(str(src), str(dst), "copy")

    assert (dst / "a.txt").read_text() == "a"


def test_hardlink_mode_same_fs(tmp_path: Path) -> None:
    src = tmp_path / "out.csv"
    src.write_text("data")
    dst = tmp_path / "in.csv"

    used = materialize(str(src), str(dst), "hardlink")

    assert used == "hardlink"
    assert os.path.samefile(str(src), str(dst))


def test_symlink_mode(tmp_path: Path) -> None:
    src = tmp_path / "out.csv"
    src.write_text("data")
    dst = tmp_path / "in.csv"

    used = materialize(str(src), str(dst), "symlink")

    assert used == "symlink"
    assert dst.is_symlink()
    assert dst.read_text() == "data"


def test_overwrite_existing_target(tmp_path: Path) -> None:
    src = tmp_path / "out.csv"
    src.write_text("new")
    dst = tmp_path / "in.csv"
    dst.write_text("stale")

    materialize(str(src), str(dst), "copy")

    assert dst.read_text() == "new"


def test_overwrite_stale_symlink_target(tmp_path: Path) -> None:
    old = tmp_path / "old.csv"
    old.write_text("old")
    dst = tmp_path / "in.csv"
    dst.symlink_to(old)

    src = tmp_path / "out.csv"
    src.write_text("fresh")
    materialize(str(src), str(dst), "copy")

    assert not dst.is_symlink()
    assert dst.read_text() == "fresh"


def test_link_falls_back_to_copy_on_oserror(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    src = tmp_path / "out.csv"
    src.write_text("data")
    dst = tmp_path / "in.csv"

    def fake_link(a, b):
        raise OSError(18, "Invalid cross-device link")

    monkeypatch.setattr("pdpp.utils.materialize.os.link", fake_link)

    used = materialize(str(src), str(dst), "hardlink")

    assert used == "copy"
    assert dst.read_text() == "data"
    assert not os.path.samefile(str(src), str(dst))


def test_unknown_mode_raises(tmp_path: Path) -> None:
    src = tmp_path / "out.csv"
    src.write_text("data")

    with pytest.raises(ValueError):
        materialize(str(src), str(tmp_path / "in.csv"), "teleport")  # type: ignore[arg-type]
