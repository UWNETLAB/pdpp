"""End-to-end tests that run a real pdpp pipeline through doit.

These build a project on disk, then execute its dodo.py in a subprocess (the
same way ``pdpp run`` does), so they exercise the full task_creator ->
make_link_task -> runner -> output-tracking path.
"""

import subprocess
import sys
from pathlib import Path

import pytest

from pdpp.templates.dep_dataclass import dep_dataclass
from tests.conftest import make_standard_task

WRITE_RESULT_SRC = (
    "from pathlib import Path\n"
    "Path('../output/result.csv').write_text('generated')\n"
)

COPY_INPUT_SRC = (
    "from pathlib import Path\n"
    "data = Path('../input/result.csv').read_text()\n"
    "Path('../output/final.csv').write_text(data)\n"
)


def _run_pipeline(project: Path) -> subprocess.CompletedProcess:
    return subprocess.run(
        [sys.executable, "dodo.py"],
        cwd=project,
        capture_output=True,
        text=True,
    )


def _make_producer(project: Path, name: str) -> None:
    task = make_standard_task(name)
    task.src_files = ["run.py"]
    task.language = "Python"
    (project / name / "src" / "run.py").write_text(WRITE_RESULT_SRC)
    task.save_self()


@pytest.fixture(autouse=True)
def _has_doit() -> None:
    pytest.importorskip("doit")


def test_terminal_task_runs_and_produces_output(in_tmp_project: Path) -> None:
    _make_producer(in_tmp_project, "produce")

    result = _run_pipeline(in_tmp_project)

    assert result.returncode == 0, result.stderr + result.stdout
    assert (in_tmp_project / "produce" / "output" / "result.csv").exists()


def test_deleted_terminal_output_is_regenerated(in_tmp_project: Path) -> None:
    """DATA-5: a terminal output with no downstream consumer regenerates."""
    _make_producer(in_tmp_project, "produce")
    assert _run_pipeline(in_tmp_project).returncode == 0

    output = in_tmp_project / "produce" / "output" / "result.csv"
    assert output.exists()
    output.unlink()

    result = _run_pipeline(in_tmp_project)

    assert result.returncode == 0, result.stderr + result.stdout
    assert output.exists(), "deleted terminal output was not regenerated"


def test_disabled_upstream_blocks_enabled_downstream(in_tmp_project: Path) -> None:
    """DATA-4: enabled downstream must not silently run on stale linked data."""
    # upstream producer, but disabled
    upstream = make_standard_task("produce")
    upstream.src_files = ["run.py"]
    upstream.language = "Python"
    (in_tmp_project / "produce" / "src" / "run.py").write_text(WRITE_RESULT_SRC)
    upstream.enabled = False
    upstream.save_self()

    # downstream consumer, enabled, depends on the disabled upstream
    downstream = make_standard_task("consume")
    downstream.src_files = ["run.py"]
    downstream.language = "Python"
    downstream.dep_files["produce"] = dep_dataclass(
        task_out="output",
        task_name="produce",
        file_list=["result.csv"],
        dir_list=[],
    )
    (in_tmp_project / "consume" / "src" / "run.py").write_text(COPY_INPUT_SRC)
    downstream.save_self()

    result = _run_pipeline(in_tmp_project)

    combined = result.stdout + result.stderr
    assert result.returncode != 0, "pipeline should fail rather than use stale data"
    assert "disabled upstream" in combined
    # The downstream task must not have produced a (wrong) output.
    assert not (in_tmp_project / "consume" / "output" / "final.csv").exists()


def test_enabled_chain_runs_end_to_end(in_tmp_project: Path) -> None:
    upstream = make_standard_task("produce")
    upstream.src_files = ["run.py"]
    upstream.language = "Python"
    (in_tmp_project / "produce" / "src" / "run.py").write_text(WRITE_RESULT_SRC)
    upstream.save_self()

    downstream = make_standard_task("consume")
    downstream.src_files = ["run.py"]
    downstream.language = "Python"
    downstream.dep_files["produce"] = dep_dataclass(
        task_out="output",
        task_name="produce",
        file_list=["result.csv"],
        dir_list=[],
    )
    (in_tmp_project / "consume" / "src" / "run.py").write_text(COPY_INPUT_SRC)
    downstream.save_self()

    result = _run_pipeline(in_tmp_project)

    assert result.returncode == 0, result.stderr + result.stdout
    assert (in_tmp_project / "consume" / "output" / "final.csv").read_text() == (
        "generated"
    )
