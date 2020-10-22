from pdpp.pdpp_class_base import BasePDPPClass
from typing import List, Dict
from os import mkdir
from pdpp.utils.yaml_dump_self import yaml_dump_self
from pdpp.templates.project_structure import create_in_out_src


class StepTask(BasePDPPClass):
    """
    This is the class documentation
    """

    def __init__(
            self,
            target_dir
            ):

        self.target_dir = target_dir
        self.dep_files: Dict[str, List[str]]
        self.import_files: List
        self.src_files: List
        self.language: str
        self.enabled: bool

    FILENAME = ".pdpp_step.yaml"
    IN_DIR = "input"
    OUT_DIR = "output"
    SRC_DIR = "src"

    def initialize_step(self):
        create_in_out_src(self.target_dir)