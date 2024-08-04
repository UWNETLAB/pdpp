from typing import List

from pdpp.automation.link_task import make_link_task
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
            yield {
                "basename": f"{task.target_dir}",
                "actions": task.provide_run_actions(),
                "file_dep": dep_list,
                "targets": target_list,
                "clean": True,
            }


def task_all():
    yield gen_many_tasks()


if __name__ == "__main__":
    import doit

    doit.run(globals())
