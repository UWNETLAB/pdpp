from pdpp.pdpp_class_base import BasePDPPClass
from typing import List, Dict
from os import mkdir, DirEntry
from pdpp.utils.execute_at_target import execute_at_target
from pdpp.templates.create_in_out_src import create_in_out_src
from pdpp.utils.yaml_task import dump_self
from pdpp.utils.immediate_link import immediate_link
from pdpp.questions import *
from pdpp.languages.language_enum import Language


class StepTask(BasePDPPClass):
    """
    This is the class documentation
    """

    def __init__(
            self,
            target_dir
            ):

        self.target_dir = target_dir
        self.dep_files = {}
        self.src_files: List = []
        self.language: str = Language.PYTHON.value
        self.enabled: bool = True

    FILENAME = ".pdpp_step.yaml"
    RIG_VALID = True # Can be rigged
    TRG_VALID = True # Can have targets 
    DEP_VALID = True # Can contain dependencies for other tasks
    SRC_VALID = True # Can have source code
    IN_DIR = "input"
    OUT_DIR = "output"
    SRC_DIR = "src"

    def rig_task(self):
        from pdpp.utils.directory_test import get_dependency_tasks

        # Ask dependency questions:
        dep_tasks = get_dependency_tasks()
        selected_dep_tasks = q1(dep_tasks, self)
        self.dep_files = q2(selected_dep_tasks, self)


        # Ensure source compliance:
        self.src_files = q3(self)
        self.language = q4(self)

        immediate_link(self)

        # Finally, save self to YAML:
        execute_at_target(dump_self, self)


    def initialize_task(self):

        # Create directory structure:
        mkdir(self.target_dir)
        execute_at_target(create_in_out_src, self)

        # From here on out, rigging is identical to creating anew:
        self.rig_task()
