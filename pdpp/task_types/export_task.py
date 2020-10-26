from pdpp.pdpp_class_base import BasePDPPClass
from typing import List, Dict, Tuple
from os import mkdir
from pdpp.utils.yaml_task import dump_self
from pdpp.templates.dep_dataclass import dep_dataclass
from pdpp.utils.execute_at_target import execute_at_target


class ExportTask(BasePDPPClass):
    """
    This is the class documentation
    """

    def __init__(
            self
            ):

        self.target_dir: str = "_export_"
        self.dep_files: Dict[str, List[str]] = {}
        self.enabled: bool = True
        self.src_files: List = []


    FILENAME = ".pdpp_export.yaml"
    RIG_VALID = True # Can be rigged
    TRG_VALID = False # Can have targets 
    DEP_VALID = False # Can contain dependencies for other tasks
    SRC_VALID = False # Can have source code
    RUN_VALID = True # Has actions that should be executed at runtime
    IN_DIR = "./"
    OUT_DIR = "./"
    SRC_DIR = False

    def provide_run_actions(self) -> Tuple:
        return ()

    def provide_src_dependencies(self) -> List:
        return []

    def rig_task(self):
        pass

    def initialize_task(self):
        mkdir(self.target_dir)
        execute_at_target(dump_self, self)

    def provide_dependencies(self, other_task) -> List[str]:
        return []