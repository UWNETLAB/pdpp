from pdpp.pdpp_class_base import BasePDPPClass
from typing import List, Dict
from os import mkdir, chdir
from pdpp.utils.yaml_task import dump_self
from pdpp.utils.execute_at_target import execute_at_target

class ImportTask(BasePDPPClass):
    """
    This is the class documentation
    """

    def __init__(
            self
            ):

        self.target_dir = "_import_"
        self.enabled = True


    FILENAME = ".pdpp_import.yaml"
    RIG_VALID = False # Can be rigged
    TRG_VALID = False # Can have targets 
    DEP_VALID = True # Can contain dependencies for other tasks
    SRC_VALID = False # Can have source code
    IN_DIR = "./"
    OUT_DIR = "./"
    SRC_DIR = False


    def initialize_task(self):
        mkdir(self.target_dir)
        execute_at_target(dump_self, self)

