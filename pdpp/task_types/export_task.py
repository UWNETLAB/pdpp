from pdpp.pdpp_class_base import BasePDPPClass
from typing import List, Dict
from os import mkdir
from pdpp.utils.yaml_dump_self import yaml_dump_self


class ExportTask(BasePDPPClass):
    """
    This is the class documentation
    """

    def __init__(
            self
            ):

        self.target_dir = "_export_"
        self.dep_files: Dict[str, List[str]] = []
        self.enabled = True


    FILENAME = ".pdpp_export.yaml"
    IN_DIR = ""
    OUT_DIR = ""
    HAS_SOURCE = False


    def initialize_step(self):
        mkdir(self.target_dir)
        yaml_dump_self(self)

