"""Track task outputs so deleted terminal outputs are regenerated.

pdpp only recorded a task's *downstream-consumed* files as doit ``targets``. A
terminal task (nothing depends on it) therefore had empty targets, so doit
judged it up-to-date and silently skipped it even when its output had been
deleted.

This module records the set of files a task produced after each run (saved in
doit's own values store) and exposes an ``uptodate`` check that forces a rerun
when any previously-produced output file is missing. This works even for tasks
with no downstream consumer, because it does not rely on statically-declared
targets.
"""

import os
from posixpath import join
from typing import Any, Callable, Dict, List

from pdpp.tasks.base_task import BaseTask


def _output_dir(task: BaseTask) -> str:
    return join(task.target_dir, task.OUT_DIR)


def list_output_files(task: BaseTask) -> List[str]:
    """Return a sorted list of every file currently under the task's output."""
    out_dir = _output_dir(task)
    found: List[str] = []
    for root, _, files in os.walk(out_dir):
        for filename in files:
            found.append(join(root, filename))
    return sorted(found)


def make_output_recorder(task: BaseTask) -> Callable[[], Dict[str, List[str]]]:
    """Build a doit action that records the task's produced output files."""

    def record_outputs() -> Dict[str, List[str]]:
        return {"produced_outputs": list_output_files(task)}

    return record_outputs


def make_outputs_present_check(
    task: BaseTask,
) -> Callable[[Any, Dict[str, Any]], bool]:
    """Build a doit ``uptodate`` check: False if any recorded output is gone."""

    def outputs_present(task: Any, values: Dict[str, Any]) -> bool:
        produced = values.get("produced_outputs")
        if produced is None:
            # Never recorded (task has not run under this scheme yet).
            return False
        return all(os.path.exists(path) for path in produced)

    return outputs_present
