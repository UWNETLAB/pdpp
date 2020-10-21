from pdpp.pdpp_class_base import BasePDPPClass
from typing import List, Dict


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

    filename = ".pdpp_project.yaml"
    in_dir = "_import_"
    out_dir = "_export_"
    has_source = False

    def initialize_step(self):
        populate_new_project(self.target_dir)