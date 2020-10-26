from typing import Dict, List, Union
from abc import ABC, abstractmethod
from pdpp.templates.dep_dataclass import dep_dataclass


class BasePDPPClass(ABC):
    """
    This is a docstring.
    """
    def __init__(
        self
        ):

        self.target_dir: str
        self.language: str
        self.enabled: bool    
        self.dep_files: Dict[str, dep_dataclass]
        self.import_files: List
        self.src_files: List

    
    FILENAME = ".pdpp_export.yaml"
    RIG_VALID = True # Can be rigged
    TRG_VALID = False # Can have targets 
    DEP_VALID = True # Can contain dependencies for other tasks
    SRC_VALID = False # Can have source code
    RUN_VALID = True # Has actions that should be executed at runtime
    IN_DIR: str
    OUT_DIR: str
    SRC_DIR: str
    

    @abstractmethod
    def provide_dependencies(self, other_task) -> List[str]:
        pass

    @abstractmethod
    def rig_task(self):
        pass

    @abstractmethod
    def initialize_task(self):
        pass

