from pdpp.pdpp_class_base import BasePDPPClass
from typing import List, Dict, Tuple
from os import mkdir, chdir
from pdpp.utils.yaml_task import dump_self
from pdpp.templates.populate_new_project import populate_new_project
from pdpp.templates.dep_dataclass import dep_dataclass


class SubTask(BasePDPPClass):
    """
    This is the class documentation
    """
    def __init__(
            self,
            target_dir = '',
            dep_files = {},
            enabled = True):
        
        self.target_dir = target_dir
        self.dep_files: Dict[str, List[str]] = dep_files
        self.enabled = enabled
        self.has_source = False
        self.src_files: List = []

    FILENAME = ".pdpp_project.yaml"
    RIG_VALID = True # Can be rigged
    TRG_VALID = True # Can have targets 
    DEP_VALID = True # Can contain dependencies for other tasks
    SRC_VALID = False # Can have source code
    RUN_VALID = True # Has actions that should be executed at runtime
    IN_DIR = "_import_"
    OUT_DIR = "_export_"
    SRC_DIR = False

    def provide_run_actions(self) -> Tuple:
        return ()
        
    def provide_src_dependencies(self) -> List:
        return []

    def rig_task(self):
        pass

    def initialize_task(self):
        populate_new_project()

    def provide_dependencies(self, other_task) -> List[str]:
        return []
