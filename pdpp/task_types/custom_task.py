from pdpp.pdpp_class_base import BasePDPPClass
from typing import List, Dict
from os import chdir
        

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
    IN_DIR = "input"
    OUT_DIR = "output"
    SRC_DIR = "src"

    def initialize_step(self):
        create_in_out_src(self.target_dir)
