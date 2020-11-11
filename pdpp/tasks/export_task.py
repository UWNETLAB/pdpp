from pdpp.tasks.base_task import BaseTask
from typing import List, Dict
from os import mkdir
from pdpp.utils.execute_at_target import execute_at_target
from pdpp.utils.yaml_task import dump_self
from pdpp.languages.language_enum import Language
from pdpp.templates.dep_dataclass import dep_dataclass


class ExportTask(BaseTask):
    """
    This is the class documentation
    """

    def __init__(
            self,
            target_dir: str = "_export_"
            ):

        self.target_dir: str = "_export_"
        self.dep_files: Dict[str, dep_dataclass] = {}
        self.src_files: List = []
        self.language: str = Language.NULL.value
        self.enabled: bool = True


    RIG_VALID = True # Can be rigged
    TRG_VALID = False # Can have targets 
    DEP_VALID = False # Can contain dependencies for other tasks
    SRC_VALID = False # Should soucre code be automatically parsed?
    RUN_VALID = False # Has actions that should be executed at runtime
    IN_DIR = "./"
    OUT_DIR = "./"
    SRC_DIR = "./"

    def initialize_task(self):
        mkdir(self.target_dir)
        execute_at_target(dump_self, self)
