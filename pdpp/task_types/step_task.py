from pdpp.pdpp_class_base import BasePDPPClass
from typing import List, Dict
from posixpath import join


class StepTask(BasePDPPClass):
    """
    This is the class documentation
    """

    def __init__(
            self, 
            target_dir = '',
            dep_files = {}, 
            import_files = [],
            src_files = [], 
            language = '', 
            enabled = True,
            ):

        self.target_dir = target_dir
        self.dep_files: Dict[str, List[str]] = dep_files
        self.import_files = import_files
        self.src_files = src_files
        self.language = language
        self.enabled = enabled

    filename = ".pdpp_step.yaml"
    in_dir = "input"
    out_dir = "output"
    src_dir = "src"
    has_source = True

    def initialize_step(self):
        create_in_out_src(self.target_dir)
        self.src_files.append(join(self.target_dir, "src", (self.target_dir + ".py")))