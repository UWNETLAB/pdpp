from pathlib import Path

import pytest

LEGACY_STANDARD_TASK = """\
!!python/object:pdpp.tasks.standard_task.StandardTask
dep_files:
  clean: !!python/object:pdpp.templates.dep_dataclass.dep_dataclass
    dir_list: []
    file_list:
    - data.csv
    task_name: clean
    task_out: output
enabled: true
language: Python
src_files:
- analyze.py
target_dir: analyze
"""

LEGACY_IMPORT_TASK = """\
!!python/object:pdpp.tasks.import_task.ImportTask
dep_files: {}
enabled: true
language: ''
src_files: []
target_dir: _import_
"""

LEGACY_EXPORT_TASK = """\
!!python/object:pdpp.tasks.export_task.ExportTask
dep_files:
  analyze: !!python/object:pdpp.templates.dep_dataclass.dep_dataclass
    dir_list: []
    file_list:
    - results.csv
    task_name: analyze
    task_out: output
enabled: true
language: ''
src_files: []
target_dir: _export_
"""


@pytest.fixture
def in_tmp_project(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> Path:
    """Create a minimal pdpp project skeleton in tmp_path and chdir into it."""
    monkeypatch.chdir(tmp_path)
    (tmp_path / "dodo.py").write_text(
        "from pdpp.automation.task_creator import gen_many_tasks, task_all\n"
        "import doit\n"
        "doit.run(globals())\n"
    )
    for boundary in ("_import_", "_export_"):
        (tmp_path / boundary).mkdir()
    return tmp_path


def make_standard_task(target_dir: str):
    """Build a StandardTask with directories on disk (no prompts)."""
    from pdpp.tasks.standard_task import StandardTask

    task = StandardTask(target_dir=target_dir)
    for sub in ("input", "output", "src"):
        Path(target_dir, sub).mkdir(parents=True, exist_ok=True)
    return task


def add_dependency(task, upstream, file_list=None, dir_list=None) -> None:
    """Record `upstream` as a dependency of `task` (no prompts)."""
    from pdpp.templates.dep_dataclass import dep_dataclass

    task.dep_files[upstream.target_dir] = dep_dataclass(
        task_out=upstream.OUT_DIR,
        task_name=upstream.target_dir,
        file_list=list(file_list or []),
        dir_list=list(dir_list or []),
    )
