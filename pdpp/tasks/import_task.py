from os import mkdir
from typing import Dict, List

from pdpp.languages.language_enum import Language
from pdpp.tasks.base_task import BaseTask
from pdpp.templates.dep_dataclass import dep_dataclass
from pdpp.utils.execute_at_target import execute_at_target
from pdpp.utils.yaml_task import dump_self


class ImportTask(BaseTask):
    """
    This is the class documentation
    """

    def __init__(self, target_dir: str = "_import_"):
        self.target_dir: str = "_import_"
        self.dep_files: Dict[str, dep_dataclass] = {}
        self.src_files: List = []
        self.language: str = Language.NULL.value
        self.enabled: bool = True

    RIG_VALID = False  # Can be rigged
    TRG_VALID = True  # Can have targets
    DEP_VALID = True  # Can contain dependencies for other tasks
    SRC_VALID = False  # Should soucre code be automatically parsed?
    RUN_VALID = False  # Has actions that should be executed at runtime
    IN_DIR = "./"
    OUT_DIR = "./"
    SRC_DIR = "./"

    def rig_task(self):
        raise NotImplementedError

    def provide_dependencies(self, asking_task: BaseTask) -> List[str]:
        return []

    def initialize_task(self):
        mkdir(self.target_dir)
        execute_at_target(dump_self, self)
