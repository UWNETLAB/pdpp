from os import mkdir
from posixpath import join
from typing import Dict, List

from pdpp.languages.language_enum import Language
from pdpp.languages.language_parser import parse_language
from pdpp.tasks.base_task import BaseTask
from pdpp.templates.create_in_out_src import create_in_out_src
from pdpp.templates.dep_dataclass import dep_dataclass
from pdpp.utils.execute_at_target import execute_at_target


class StandardTask(BaseTask):
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
    SRC_VALID = True  # Should soucre code be automatically parsed?
    RUN_VALID = True  # Has actions that should be executed at runtime
    IN_DIR = "input"
    OUT_DIR = "output"
    SRC_DIR = "src"

    def provide_run_actions(self) -> List:
        runner = parse_language(self)

        return [(runner, [s, self], {}) for s in self.src_files]

    def provide_src_dependencies(self) -> List:
        return [join(self.target_dir, self.SRC_DIR, s) for s in self.src_files]

    def initialize_task(self):
        # Create directory structure:
        mkdir(self.target_dir)
        execute_at_target(create_in_out_src, self)

        # From here on out, rigging is identical to creating anew:
        self.rig_task()
