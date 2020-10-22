from pdpp.pdpp_class_base import BasePDPPClass
from typing import List, Dict
from os import mkdir
from pdpp.utils.yaml_task import dump_self



class ExportTask(BasePDPPClass):
    """
    This is the class documentation
    """

    def __init__(
            self
            ):

        self.target_dir: str = "_export_"
        self.dep_files: Dict[str, List[str]]
        self.enabled: bool = True


    FILENAME = ".pdpp_export.yaml"
    RIG_VALID = True # Can be rigged
    TRG_VALID = True # Can have targets 
    DEP_VALID = False # Can contain dependencies for other tasks
    SRC_VALID = False # Can have source code
    IN_DIR = "./"
    OUT_DIR = "./"
    SRC_DIR = False


    def initialize_task(self):
        mkdir(self.target_dir)
        dump_self(self)


