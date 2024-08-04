from os import mkdir
from typing import Dict, List

from pdpp.languages.language_enum import Language
from pdpp.languages.runners import project_runner
from pdpp.tasks.base_task import BaseTask
from pdpp.templates.dep_dataclass import dep_dataclass
from pdpp.templates.populate_new_project import populate_new_project
from pdpp.utils.execute_at_target import execute_at_target


class SubTask(BaseTask):
    """
    This is the class documentation
    """

    def __init__(self, target_dir: str = ""):
        self.target_dir: str = target_dir
        self.dep_files: Dict[str, dep_dataclass] = {}
        self.src_files: List = []
        self.language: str = Language.NULL.value
        self.enabled: bool = True

    RIG_VALID = True  # Can be rigged
    TRG_VALID = True  # Can have targets
    DEP_VALID = True  # Can contain dependencies for other tasks
    SRC_VALID = False  # Should soucre code be automatically parsed?
    RUN_VALID = True  # Has actions that should be executed at runtime
    IN_DIR = "_import_"
    OUT_DIR = "_export_"
    SRC_DIR = "./"

    def provide_run_actions(self) -> List:
        return [(project_runner, [self], {})]

    def initialize_task(self):
        # Create directory structure:
        mkdir(self.target_dir)
        execute_at_target(populate_new_project, self)

        # From here on out, rigging is identical to creating anew:
        self.rig_task()
