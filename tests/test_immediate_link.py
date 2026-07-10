from pathlib import Path

import pytest

from pdpp.templates.dep_dataclass import dep_dataclass
from pdpp.utils.immediate_link import immediate_link
from tests.conftest import make_standard_task


@pytest.fixture
def rigged_pair(in_tmp_project: Path):
    """upstream 'clean' with an output file, downstream 'analyze' depending on it."""
    make_standard_task("clean")
    (in_tmp_project / "clean" / "output" / "data.csv").write_text("payload")

    downstream = make_standard_task("analyze")
    downstream.dep_files["clean"] = dep_dataclass(
        task_out="output",
        task_name="clean",
        file_list=["data.csv"],
        dir_list=[],
    )
    return in_tmp_project, downstream


def test_immediate_link_materializes_dependency(rigged_pair) -> None:
    project, downstream = rigged_pair

    immediate_link(downstream)

    linked = project / "analyze" / "input" / "data.csv"
    assert linked.read_text() == "payload"


def test_immediate_link_preserves_unmanaged_user_file(rigged_pair) -> None:
    project, downstream = rigged_pair
    user_file = project / "analyze" / "input" / "my_notes.txt"
    user_file.write_text("do not delete me")

    immediate_link(downstream)

    assert user_file.exists()
    assert user_file.read_text() == "do not delete me"


def test_immediate_link_default_copy_does_not_alias(rigged_pair) -> None:
    project, downstream = rigged_pair
    immediate_link(downstream)

    linked = project / "analyze" / "input" / "data.csv"
    linked.write_text("edited downstream")

    upstream_out = project / "clean" / "output" / "data.csv"
    assert upstream_out.read_text() == "payload"
