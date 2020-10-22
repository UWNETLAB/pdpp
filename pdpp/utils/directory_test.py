from posixpath import exists, join
from os import DirEntry, chdir, scandir, listdir
from pdpp.pdpp_class_base import BasePDPPClass
from pdpp.task_types import all_task_filenames
#from pdpp.utils.import_step_class import import_step_class
from typing import List
from itertools import compress


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


def riggable_directory_test(dir_) -> List[str]:
    """
    This function tests a directory to see if it is a valid pdpp-compliant step directory.
    Returns 'True' if all three aforementioned subdirectories are found, returns 'False' otherwise. 
    """

    return list(compress(all_task_filenames, list(map(exists, [join(dir_, n) for n in all_task_filenames]))))


def get_riggable_directories() -> List:
    """
    Returns a list of all the riggable directories at this level of the project (or subproject)
    """

    return [(f, riggable_directory_test(f)) for f in [r.name for r in scandir() if r.is_dir()] if riggable_directory_test(f)]


def get_riggable_classes() -> List[BasePDPPClass]:
    directories = get_riggable_directories()

    classes = []

    for directory in directories:
        for _class in all_task_types:
            if exists(join(directory, _class.filename)):
                classes.append(import_step_class(directory, _class.filename))

    return classes, directories

