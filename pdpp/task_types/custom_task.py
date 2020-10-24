from pdpp.pdpp_class_base import BasePDPPClass
from typing import List, Dict
from os import mkdir
from pdpp.utils.yaml_task import dump_self
from pdpp.templates.create_in_out_src import create_in_out_src
from pdpp.utils.execute_at_target import execute_at_target


class CustomTask(BasePDPPClass):
    """
    This is the class documentation
    """
    def __init__(
            self, 
            target_dir = '',
            dep_files = {}, 
            import_files = [],
            shell_commands = [],
            enabled = True
            ):

        self.target_dir = target_dir
        self.dep_files: Dict[str, List[str]] = dep_files
        self.import_files = import_files
        self.shell_commands = []
        self.enabled = enabled

    FILENAME = ".pdpp_custom.yaml"
    RIG_VALID = True # Can be rigged
    TRG_VALID = True # Can have targets 
    DEP_VALID = True # Can contain dependencies for other tasks
    SRC_VALID = True # Can have source code
    IN_DIR = "input"
    OUT_DIR = "output"
    SRC_DIR = "src"

    def rig_task(self):
        pass
    
    def initialize_task(self):
        execute_at_target(create_in_out_src, self)
