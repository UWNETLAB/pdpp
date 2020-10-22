from pdpp.pdpp_class_base import BasePDPPClass
from typing import List, Dict
from os import mkdir
from pdpp.utils.yaml_dump_self import yaml_dump_self


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
    IN_DIR = ""
    OUT_DIR = ""
    SRC_DIR = False


    def initialize_step(self):
        mkdir(self.target_dir)
        yaml_dump_self(self)

