from pdpp.pdpp_class_base import BasePDPPClass
from typing import List, Dict
from os import mkdir, chdir
from pdpp.utils.yaml_task import dump_self
from pdpp.templates.populate_new_project import populate_new_project

class SubTask(BasePDPPClass):
    """
    This is the class documentation
    """
    def __init__(
            self,
            target_dir = '',
            dep_files = {},
            import_files = [],
            enabled = True):
        
        self.target_dir = target_dir
        self.dep_files: Dict[str, List[str]] = dep_files
        self.import_files = import_files
        self.enabled = enabled
        self.has_source = False

    FILENAME = ".pdpp_project.yaml"
    RIG_VALID = True # Can be rigged
    TRG_VALID = True # Can have targets 
    DEP_VALID = True # Can contain dependencies for other tasks
    SRC_VALID = False # Can have source code
    IN_DIR = "_import_"
    OUT_DIR = "_export_"
    SRC_DIR = False

    def rig_task(self):
        pass

    def initialize_task(self):
        populate_new_project()