from pathlib import Path

import pytest
import yaml

from pdpp.tasks.custom_task import CustomTask
from pdpp.tasks.export_task import ExportTask
from pdpp.tasks.import_task import ImportTask
from pdpp.tasks.standard_task import StandardTask
from pdpp.tasks.sub_task import SubTask
from pdpp.templates.dep_dataclass import dep_dataclass
from pdpp.utils.yaml_task import SCHEMA_VERSION, dump_self, load_task, task_to_dict
from tests.conftest import (
    LEGACY_EXPORT_TASK,
    LEGACY_IMPORT_TASK,
    LEGACY_STANDARD_TASK,
)


class TestMaliciousPayloadRejection:
    def test_object_apply_payload_rejected_without_side_effects(
        self, tmp_path: Path
    ) -> None:
        marker = tmp_path / "PWNED"
        payload = tmp_path / ".pdpp_task.yaml"
        payload.write_text(
            f'!!python/object/apply:os.system ["touch {marker}"]\n'
        )

        with pytest.raises(yaml.constructor.ConstructorError):
            load_task(str(payload))

        assert not marker.exists()

    def test_object_new_payload_rejected(self, tmp_path: Path) -> None:
        payload = tmp_path / ".pdpp_task.yaml"
        payload.write_text(
            "!!python/object/new:os.system\nargs: ['echo hi']\n"
        )

        with pytest.raises(yaml.constructor.ConstructorError):
            load_task(str(payload))

    def test_nested_malicious_tag_inside_legit_task_rejected(
        self, tmp_path: Path
    ) -> None:
        marker = tmp_path / "PWNED_NESTED"
        payload = tmp_path / ".pdpp_task.yaml"
        payload.write_text(
            "!!python/object:pdpp.tasks.standard_task.StandardTask\n"
            "target_dir: analyze\n"
            "dep_files:\n"
            f'  evil: !!python/object/apply:os.system ["touch {marker}"]\n'
        )

        with pytest.raises(yaml.constructor.ConstructorError):
            load_task(str(payload))

        assert not marker.exists()

    def test_arbitrary_python_object_tag_rejected(self, tmp_path: Path) -> None:
        payload = tmp_path / ".pdpp_task.yaml"
        payload.write_text("!!python/object:pathlib.Path {}\n")

        with pytest.raises(yaml.constructor.ConstructorError):
            load_task(str(payload))

    def test_non_task_plain_yaml_rejected(self, tmp_path: Path) -> None:
        payload = tmp_path / ".pdpp_task.yaml"
        payload.write_text("just_a_key: just_a_value\n")

        with pytest.raises(ValueError):
            load_task(str(payload))


class TestLegacyCompatibility:
    def test_legacy_standard_task_loads(self, tmp_path: Path) -> None:
        path = tmp_path / ".pdpp_task.yaml"
        path.write_text(LEGACY_STANDARD_TASK)

        task = load_task(str(path))

        assert isinstance(task, StandardTask)
        assert task.target_dir == "analyze"
        assert task.enabled is True
        assert task.language == "Python"
        assert task.src_files == ["analyze.py"]
        dep = task.dep_files["clean"]
        assert isinstance(dep, dep_dataclass)
        assert dep.task_name == "clean"
        assert dep.task_out == "output"
        assert dep.file_list == ["data.csv"]
        assert dep.dir_list == []

    def test_legacy_import_task_loads(self, tmp_path: Path) -> None:
        path = tmp_path / ".pdpp_task.yaml"
        path.write_text(LEGACY_IMPORT_TASK)

        task = load_task(str(path))

        assert isinstance(task, ImportTask)
        assert task.target_dir == "_import_"

    def test_legacy_export_task_loads(self, tmp_path: Path) -> None:
        path = tmp_path / ".pdpp_task.yaml"
        path.write_text(LEGACY_EXPORT_TASK)

        task = load_task(str(path))

        assert isinstance(task, ExportTask)
        assert task.dep_files["analyze"].file_list == ["results.csv"]

    @pytest.mark.parametrize(
        "tag_module, cls",
        [
            ("custom_task.CustomTask", CustomTask),
            ("sub_task.SubTask", SubTask),
        ],
    )
    def test_legacy_other_task_types_load(
        self, tmp_path: Path, tag_module: str, cls: type
    ) -> None:
        path = tmp_path / ".pdpp_task.yaml"
        path.write_text(
            f"!!python/object:pdpp.tasks.{tag_module}\n"
            "target_dir: mytask\n"
            "dep_files: {}\n"
            "src_files: []\n"
            "language: ''\n"
            "enabled: false\n"
        )

        task = load_task(str(path))

        assert isinstance(task, cls)
        assert task.target_dir == "mytask"
        assert task.enabled is False


class TestNewFormat:
    def _example_task(self) -> StandardTask:
        task = StandardTask(target_dir="analyze")
        task.src_files = ["analyze.py"]
        task.language = "Python"
        task.enabled = True
        task.dep_files = {
            "clean": dep_dataclass(
                task_out="output",
                task_name="clean",
                file_list=["data.csv"],
                dir_list=["models"],
            )
        }
        return task

    def test_round_trip_preserves_all_fields(
        self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        monkeypatch.chdir(tmp_path)
        task = self._example_task()

        dump_self(task)
        loaded = load_task(StandardTask.FILENAME)

        assert isinstance(loaded, StandardTask)
        assert loaded.target_dir == task.target_dir
        assert loaded.src_files == task.src_files
        assert loaded.language == task.language
        assert loaded.enabled == task.enabled
        assert loaded.dep_files.keys() == task.dep_files.keys()
        assert loaded.dep_files["clean"] == task.dep_files["clean"]

    def test_dump_contains_no_python_object_tags(
        self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        monkeypatch.chdir(tmp_path)
        dump_self(self._example_task())

        text = Path(StandardTask.FILENAME).read_text()

        assert "!!python" not in text
        assert f"schema_version: {SCHEMA_VERSION}" in text
        assert "task_type: StandardTask" in text

    def test_dump_is_safe_loadable(
        self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        monkeypatch.chdir(tmp_path)
        dump_self(self._example_task())

        data = yaml.safe_load(Path(StandardTask.FILENAME).read_text())

        assert data == task_to_dict(self._example_task())

    def test_dump_replaces_atomically_leaving_no_tmp_file(
        self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        monkeypatch.chdir(tmp_path)
        dump_self(self._example_task())

        assert not Path(StandardTask.FILENAME + ".tmp").exists()

    def test_unknown_task_type_rejected(self, tmp_path: Path) -> None:
        path = tmp_path / ".pdpp_task.yaml"
        path.write_text(
            "schema_version: 1\ntask_type: EvilTask\ntarget_dir: x\n"
        )

        with pytest.raises(ValueError):
            load_task(str(path))
