from typing import Dict, List
from abc import ABC, abstractmethod


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
        self.dep_files: Dict[str, List[str]] 
        self.import_files: List
        self.src_files: List

    
    FILENAME: str
    IN_DIR: str
    OUT_DIR: str
    HAS_SOURCE: bool
    

    @abstractmethod
    def initialize_step(self):
        pass
