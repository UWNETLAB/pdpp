from posixpath import exists, join
from os import DirEntry, scandir, listdir
from pdpp.pdpp_class import base_pdpp_class, export_class, custom_class, project_class, step_class
from pdpp.utils.import_step_class import import_step_class
from typing import List
 
pdpp_classes_list = [export_class, custom_class, project_class, step_class]

class NotInProjectException(Exception):
    """
    Raised when a user attempts to use most pdpp commands from outside project folder (project folders contain a dodo.py file)
    """
    pass

def in_project_folder():

    if exists("dodo.py") and len(listdir()) > 0:
        pass
    # elif len(listdir()) == 0:
    #     pass
    else:
        print("""Please run this command from an empty directory or an existing project directory (project directories contain a dodo.py file)""")
        raise NotInProjectException


def get_riggable_directories() -> list:
    """
    Returns a list of all the riggable directories at this level of the project (or subproject)
    """
    riggables = [f.path.replace('./', '').replace('.\\', '') for f in scandir() if riggable_directory_test(f)]

    return riggables

def get_riggable_classes() -> List[base_pdpp_class]:
    directories = get_riggable_directories()

    classes = []

    for directory in directories:
        for _class in pdpp_classes_list:
            if exists(join(directory, _class.filename)):
                classes.append(import_step_class(directory, _class.filename))

    return classes

def riggable_directory_test(dirs:DirEntry) -> bool:
    """
    This function tests a directory to see if it is a valid pdpp-compliant step directory; this is defined as any directory containing one of the following YAML files:

    "pdpp_step.yaml"
    "pdpp_export.yaml"
    "pdpp_custom.yaml"
    "pdpp_project.yaml"

    Returns 'True' if all three aforementioned subdirectories are found, returns 'False' otherwise. 

    """

    for _class in pdpp_classes_list:
        if exists(join(dirs, _class.filename)):
            return True

    return False