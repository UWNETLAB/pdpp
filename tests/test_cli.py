from pathlib import Path

import pytest
import yaml
from click.testing import CliRunner

from pdpp.main import main

NON_PROJECT_COMMANDS = [
    ["run"],
    ["graph", "-f", "png", "-s", "default"],
    ["enable"],
    ["rig"],
    ["custom", "-s", "foo"],
    ["sub", "-s", "foo"],
    ["extant"],
    ["migrate"],
]


@pytest.mark.parametrize("argv", NON_PROJECT_COMMANDS)
def test_command_outside_project_exits_cleanly(
    argv, tmp_path: Path, monkeypatch
) -> None:
    monkeypatch.chdir(tmp_path)

    result = CliRunner().invoke(main, argv)

    assert result.exit_code != 0
    assert "Traceback" not in result.output
    assert "project directory" in result.output


def test_help_lists_migrate_command() -> None:
    result = CliRunner().invoke(main, ["--help"])

    assert result.exit_code == 0
    assert "migrate" in result.output


def test_init_creates_new_format_project(tmp_path: Path, monkeypatch) -> None:
    monkeypatch.chdir(tmp_path)

    result = CliRunner().invoke(main, ["init"])

    assert result.exit_code == 0, result.output
    assert (tmp_path / "dodo.py").exists()
    assert (tmp_path / ".gitignore").exists()

    for boundary in ("_import_", "_export_"):
        task_file = tmp_path / boundary / ".pdpp_task.yaml"
        assert task_file.exists()
        text = task_file.read_text()
        assert "!!python" not in text
        assert yaml.safe_load(text)["schema_version"] == 1


def test_new_task_metadata_uses_safe_format(tmp_path: Path, monkeypatch) -> None:
    monkeypatch.chdir(tmp_path)
    CliRunner().invoke(main, ["init"])

    # `new` requires an interactive rig; drive it non-interactively instead by
    # constructing the task directly, then confirm the on-disk format is safe.
    from tests.conftest import make_standard_task

    task = make_standard_task("analyze")
    task.save_self()

    text = (tmp_path / "analyze" / ".pdpp_task.yaml").read_text()
    assert "!!python" not in text
    assert yaml.safe_load(text)["task_type"] == "StandardTask"
