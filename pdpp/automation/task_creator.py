from typing import List

from pdpp.automation.link_task import make_link_task
from pdpp.automation.output_tracking import (
    make_output_recorder,
    make_outputs_present_check,
)
from pdpp.tasks.base_task import BaseTask
from pdpp.utils.directory_test import get_pdpp_tasks


def find_dependencies_from_others(
    task: BaseTask, loaded_tasks: List[BaseTask]
) -> List[str]:
    dependencies = []

    for other_task in loaded_tasks:
        dependencies.extend(other_task.provide_dependencies(task))

    # This is just a hackier way of unpacking everything
    # pylance type-checking REALLY didn't like list(set(dependencies)) for some reason
    return [d for d in set(dependencies)]


def make_stale_upstream_failer(task: BaseTask, disabled_upstreams: List[str]):
    """Build a doit action that fails a task depending on disabled upstreams.

    Returning ``False`` makes doit report the task as failed and stop, instead
    of silently running the task on stale linked inputs (DATA-4).
    """

    def fail_stale() -> bool:
        names = ", ".join(sorted(disabled_upstreams))
        print(
            f"Task '{task.target_dir}' depends on disabled upstream task(s): "
            f"{names}. Its inputs may be stale, so pdpp refuses to run it. "
            f"Re-enable the upstream task(s) with 'pdpp enable', or disable "
            f"'{task.target_dir}' as well, then run again."
        )
        return False

    return fail_stale


def gen_many_tasks():
    # 1. Get all of the tasks in the current scope
    loaded_tasks = get_pdpp_tasks()

    # 2. Create a list of all the disabled tasks loaded in task #1
    disabled_list = [t.target_dir for t in loaded_tasks if not t.enabled]

    for task in loaded_tasks:
        target_list = find_dependencies_from_others(task, loaded_tasks)

        # Although it's hacky, 'dep_list' is altered inside of 'make_link_task'.
        # Doit places strict requirements on the format used by
        # task information, and the use of the nested 'yield' statements
        # make it difficult to get data out of the 'make_link_task' function
        # in a pythonic way. May the most exalted one - our BDFL - take pity upon me.

        dep_list = task.provide_src_dependencies()

        yield make_link_task(task, disabled_list, dep_list)

        if task.enabled and task.RUN_VALID:
            # DATA-4: if this enabled task depends on a disabled upstream task,
            # its linked inputs are stale. Refuse to run rather than silently
            # producing wrong results.
            disabled_upstreams = [
                upstream
                for upstream in task.dep_files
                if upstream in disabled_list
            ]
            if disabled_upstreams:
                yield {
                    "basename": f"{task.target_dir}",
                    "actions": [make_stale_upstream_failer(task, disabled_upstreams)],
                    "uptodate": [False],
                }
                continue

            run_task = {
                "basename": f"{task.target_dir}",
                "actions": task.provide_run_actions(),
                "file_dep": dep_list,
                "targets": target_list,
                "clean": True,
            }

            # DATA-5: also track this task's own output files so a deleted
            # terminal output (one no downstream task consumes) is regenerated
            # instead of being reported up-to-date.
            if task.TRG_VALID:
                run_task["actions"] = list(run_task["actions"]) + [
                    make_output_recorder(task)
                ]
                run_task["uptodate"] = [make_outputs_present_check(task)]

            yield run_task


def task_all():
    yield gen_many_tasks()


if __name__ == "__main__":
    import doit

    doit.run(globals())
