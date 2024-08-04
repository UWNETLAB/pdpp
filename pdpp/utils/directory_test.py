from os import listdir, scandir
from posixpath import exists, join
from typing import Iterator, List, Tuple

from pdpp.tasks.base_task import BaseTask
from pdpp.utils.yaml_task import load_task


class NotInProjectException(Exception):
    """
    Raised when a user attempts to use most pdpp commands from outside project
    directory (project directories contain a dodo.py file)
    """

    pass


def in_project_directory():
    if exists("dodo.py") and len(listdir()) > 0:
        pass

    else:
        print(
            (
                "Please run this command from an existing project directory "
                "(project directories contain a dodo.py file)"
            )
        )
        raise NotInProjectException


def pdpp_directory_test(dir_) -> bool:
    """
    This function tests a directory to see if it is a valid pdpp-compliant task directory.
    """

    return exists(join(dir_, BaseTask.FILENAME))


def get_pdpp_directories() -> Iterator[Tuple[str]]:
    """
    Returns a list of all the riggable directories at this level of the project
    (or subproject)
    """

    return zip(
        *[
            (f, BaseTask.FILENAME)
            for f in [r.name for r in scandir() if r.is_dir()]
            if pdpp_directory_test(f)
        ]
    )


def get_pdpp_tasks() -> List[BaseTask]:
    """
    Returns a list containing loaded instances of all pdpp tasks in the current
    project. (Does not recursively search subprojects).
    """

    directories, filenames = get_pdpp_directories()

    return [load_task(task) for task in map(join, directories, filenames)]


def get_riggable_tasks() -> List[BaseTask]:
    return [task for task in get_pdpp_tasks() if task.RIG_VALID]


def get_dependency_tasks() -> List[BaseTask]:
    return [task for task in get_pdpp_tasks() if task.DEP_VALID]


def get_target_tasks() -> List[BaseTask]:
    return [task for task in get_pdpp_tasks() if task.TRG_VALID]


def get_runnable_tasks() -> List[BaseTask]:
    return [task for task in get_pdpp_tasks() if task.RUN_VALID]
