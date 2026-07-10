from pathlib import Path

import yaml
from click.testing import CliRunner

from pdpp.main import main
from pdpp.tasks.standard_task import StandardTask
from pdpp.utils.yaml_task import SCHEMA_VERSION, load_task
from tests.conftest import LEGACY_IMPORT_TASK, LEGACY_STANDARD_TASK


def _write_legacy_project(project: Path) -> None:
    (project / "_import_").mkdir(exist_ok=True)
    (project / "_import_" / ".pdpp_task.yaml").write_text(LEGACY_IMPORT_TASK)
    analyze = project / "analyze"
    for sub in ("input", "output", "src"):
        (analyze / sub).mkdir(parents=True, exist_ok=True)
    (analyze / ".pdpp_task.yaml").write_text(LEGACY_STANDARD_TASK)


def test_migrate_rewrites_legacy_files_to_new_format(in_tmp_project: Path) -> None:
    _write_legacy_project(in_tmp_project)

    result = CliRunner().invoke(main, ["migrate"])

    assert result.exit_code == 0, result.output
    for task_file in ("_import_/.pdpp_task.yaml", "analyze/.pdpp_task.yaml"):
        text = (in_tmp_project / task_file).read_text()
        assert "!!python" not in text
        assert yaml.safe_load(text)["schema_version"] == SCHEMA_VERSION


def test_migrate_preserves_task_contents(in_tmp_project: Path) -> None:
    _write_legacy_project(in_tmp_project)
    before = load_task(str(in_tmp_project / "analyze" / ".pdpp_task.yaml"))

    result = CliRunner().invoke(main, ["migrate"])
    assert result.exit_code == 0, result.output

    after = load_task(str(in_tmp_project / "analyze" / ".pdpp_task.yaml"))
    assert isinstance(after, StandardTask)
    assert after.target_dir == before.target_dir
    assert after.src_files == before.src_files
    assert after.language == before.language
    assert after.enabled == before.enabled
    assert after.dep_files == before.dep_files


def test_migrate_is_idempotent(in_tmp_project: Path) -> None:
    _write_legacy_project(in_tmp_project)
    runner = CliRunner()

    assert runner.invoke(main, ["migrate"]).exit_code == 0
    first_pass = (in_tmp_project / "analyze" / ".pdpp_task.yaml").read_bytes()

    assert runner.invoke(main, ["migrate"]).exit_code == 0
    second_pass = (in_tmp_project / "analyze" / ".pdpp_task.yaml").read_bytes()

    assert first_pass == second_pass


def test_migrate_outside_project_fails_cleanly(
    tmp_path: Path, monkeypatch
) -> None:
    monkeypatch.chdir(tmp_path)

    result = CliRunner().invoke(main, ["migrate"])

    assert result.exit_code != 0
    assert "Traceback" not in result.output
