from posixpath import exists, join
from os import DirEntry, chdir, scandir, listdir
from pdpp.pdpp_class_base import BasePDPPClass
from pdpp.utils.yaml_task import load_task
from typing import List, Tuple, Iterator
from itertools import compress
import yaml
from pdpp.task_types import all_task_filenames

class NotInProjectException(Exception):
    """
    Raised when a user attempts to use most pdpp commands from outside project folder (project folders contain a dodo.py file)
    """
    pass


def in_project_folder():

    if exists("dodo.py") and len(listdir()) > 0:
        pass

    else:
        print("""Please run this command from an empty directory or an existing project directory (project directories contain a dodo.py file)""")
        raise NotInProjectException


def pdpp_directory_test(dir_) -> List[str]:
    """
    This function tests a directory to see if it is a valid pdpp-compliant step directory.
    Returns 'True' if all three aforementioned subdirectories are found, returns 'False' otherwise. 
    """

    return list(compress(all_task_filenames, list(map(exists, [join(dir_, n) for n in all_task_filenames]))))


def get_pdpp_directories() -> Iterator[Tuple[str]]:
    """
    Returns a list of all the riggable directories at this level of the project (or subproject)
    """

    return zip(*[(f, pdpp_directory_test(f)[0]) for f in [r.name for r in scandir() if r.is_dir()] if pdpp_directory_test(f)])


def get_pdpp_tasks() -> List[BasePDPPClass]:
    """
    Returns a list containing loaded instances of all pdpp tasks in the current 
    project. (Does not recursively search subprojects).
    """    

    directories, filenames = get_pdpp_directories()

    return [load_task(task) for task in map(join, directories, filenames)]


def get_riggable_tasks() -> List[BasePDPPClass]:

    return [task for task in get_pdpp_tasks() if task.RIG_VALID]


def get_dependency_tasks() -> List[BasePDPPClass]:

    return [task for task in get_pdpp_tasks() if task.DEP_VALID]


def get_target_tasks() -> List[BasePDPPClass]:

    return [task for task in get_pdpp_tasks() if task.TRG_VALID]