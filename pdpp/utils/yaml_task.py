"""Safe serialization for pdpp task metadata.

Historically pdpp wrote task metadata as live Python objects with
``yaml.dump`` and read them back with the unsafe ``yaml.Loader``, which
executes arbitrary code embedded in a crafted ``.pdpp_task.yaml``.

This module replaces that with:

- a restricted loader (``PdppTaskLoader``) that extends ``yaml.SafeLoader``
  with constructors for only the legacy pdpp task tags and the
  ``dep_dataclass`` tag, so existing project files keep loading while every
  other ``!!python/*`` tag is rejected; and
- a plain-dict, ``schema_version``-stamped on-disk format written with
  ``yaml.safe_dump`` and an atomic replace, so new and migrated files never
  embed Python object tags.

``pdpp migrate`` rewrites legacy files into the new format.
"""

import os
from typing import Any, Dict

import yaml

SCHEMA_VERSION = 1

_TASK_FIELDS = ("target_dir", "dep_files", "src_files", "language", "enabled")

_LEGACY_TASK_TAGS = {
    "tag:yaml.org,2002:python/object:pdpp.tasks.standard_task.StandardTask": "StandardTask",
    "tag:yaml.org,2002:python/object:pdpp.tasks.custom_task.CustomTask": "CustomTask",
    "tag:yaml.org,2002:python/object:pdpp.tasks.sub_task.SubTask": "SubTask",
    "tag:yaml.org,2002:python/object:pdpp.tasks.import_task.ImportTask": "ImportTask",
    "tag:yaml.org,2002:python/object:pdpp.tasks.export_task.ExportTask": "ExportTask",
}

_LEGACY_DEP_TAG = (
    "tag:yaml.org,2002:python/object:pdpp.templates.dep_dataclass.dep_dataclass"
)


def _task_classes() -> Dict[str, type]:
    from pdpp.tasks.custom_task import CustomTask
    from pdpp.tasks.export_task import ExportTask
    from pdpp.tasks.import_task import ImportTask
    from pdpp.tasks.standard_task import StandardTask
    from pdpp.tasks.sub_task import SubTask

    return {
        "StandardTask": StandardTask,
        "CustomTask": CustomTask,
        "SubTask": SubTask,
        "ImportTask": ImportTask,
        "ExportTask": ExportTask,
    }


def _dep_from_value(value: Any) -> Any:
    from pdpp.templates.dep_dataclass import dep_dataclass

    if isinstance(value, dep_dataclass):
        return value
    if isinstance(value, dict):
        return dep_dataclass(
            task_out=value["task_out"],
            task_name=value["task_name"],
            file_list=list(value.get("file_list") or []),
            dir_list=list(value.get("dir_list") or []),
        )
    raise ValueError(f"Invalid dependency entry in task metadata: {value!r}")


def _build_task(class_name: str, state: Dict[Any, Any]) -> Any:
    classes = _task_classes()
    if class_name not in classes:
        raise ValueError(f"Unknown pdpp task type: {class_name!r}")

    task = classes[class_name]()
    for field in _TASK_FIELDS:
        if field in state and state[field] is not None:
            setattr(task, field, state[field])

    task.dep_files = {
        key: _dep_from_value(value) for key, value in dict(task.dep_files).items()
    }
    return task


class PdppTaskLoader(yaml.SafeLoader):
    """A ``SafeLoader`` that also accepts the legacy pdpp object tags.

    Only the five pdpp task classes and ``dep_dataclass`` are
    reconstructable, via explicit whitelisted constructors. Every other
    ``!!python/*`` tag raises ``yaml.constructor.ConstructorError`` without
    executing anything.
    """


def _make_task_constructor(class_name: str):
    def _construct(loader: PdppTaskLoader, node: yaml.MappingNode) -> Any:
        state = loader.construct_mapping(node, deep=True)
        return _build_task(class_name, state)

    return _construct


def _construct_dep(loader: PdppTaskLoader, node: yaml.MappingNode) -> Any:
    return _dep_from_value(loader.construct_mapping(node, deep=True))


for _tag, _class_name in _LEGACY_TASK_TAGS.items():
    PdppTaskLoader.add_constructor(_tag, _make_task_constructor(_class_name))
PdppTaskLoader.add_constructor(_LEGACY_DEP_TAG, _construct_dep)


def task_to_dict(task: Any) -> Dict[str, Any]:
    """Represent a task as a plain, safe-dumpable dict (schema version 1)."""

    return {
        "schema_version": SCHEMA_VERSION,
        "task_type": type(task).__name__,
        "target_dir": task.target_dir,
        "dep_files": {
            key: {
                "task_out": dep.task_out,
                "task_name": dep.task_name,
                "file_list": list(dep.file_list),
                "dir_list": list(dep.dir_list),
            }
            for key, dep in task.dep_files.items()
        },
        "src_files": list(task.src_files),
        "language": task.language,
        "enabled": bool(task.enabled),
    }


def dump_self(task: Any) -> None:
    """Write ``task`` to its metadata file in the current directory.

    Emits the plain-dict schema-versioned format via ``yaml.safe_dump`` and
    replaces the file atomically so a crash mid-write cannot truncate
    existing metadata.
    """

    filename = type(task).FILENAME
    payload = yaml.safe_dump(
        task_to_dict(task), default_flow_style=False, sort_keys=True
    )
    tmp_filename = filename + ".tmp"
    with open(tmp_filename, "w") as stream:
        stream.write(payload)
    os.replace(tmp_filename, filename)


def load_task(task_path: str) -> Any:
    """Load a task from ``task_path``, accepting legacy and current formats.

    Raises ``yaml.constructor.ConstructorError`` for any non-whitelisted
    object tag (including all ``!!python/object/apply`` payloads) and
    ``ValueError`` for files that are not pdpp task metadata.
    """

    with open(task_path, "r") as stream:
        data = yaml.load(stream, Loader=PdppTaskLoader)

    if isinstance(data, dict):
        if "task_type" not in data:
            raise ValueError(f"Not a pdpp task metadata file: {task_path}")
        return _build_task(data["task_type"], data)

    if type(data).__name__ in _task_classes():
        return data

    raise ValueError(f"Not a pdpp task metadata file: {task_path}")
