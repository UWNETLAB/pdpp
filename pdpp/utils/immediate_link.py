"""Rig-time materialization of a task's declared dependencies.

This runs when a task is rigged, refreshing its ``input/`` directory to match
its declared dependencies. Unlike the previous implementation it does NOT wipe
the whole ``input/`` directory first: user files that are not managed
dependencies are left untouched, and only previously-materialized dependency
entries are refreshed. Materialization goes through the shared, portable
``materialize`` helper (copy by default, with link fallback), so it never
aliases upstream outputs and never crashes across filesystems.
"""

from posixpath import join

from pdpp.tasks.base_task import BaseTask
from pdpp.utils.materialize import materialize
from pdpp.utils.project_config import get_materialize_mode


def immediate_link(task: BaseTask) -> None:
    """Materialize ``task``'s declared dependency files into its input dir.

    Only the files and directories named in ``task.dep_files`` are (re)written.
    A materialization failure raises after leaving any unrelated user files in
    ``input/`` intact.
    """
    in_dir = join(task.target_dir, task.IN_DIR)
    mode = get_materialize_mode()

    for key, value in task.dep_files.items():
        out_dir = join(key, value.task_out)

        for file_entry in value.file_list:
            materialize(
                join(out_dir, file_entry), join(in_dir, file_entry), mode
            )

        for directory_entry in value.dir_list:
            materialize(
                join(out_dir, directory_entry),
                join(in_dir, directory_entry),
                mode,
            )
