from pdpp.pdpp_class_base import BasePDPPClass
from typing import List, Dict, Tuple
from os import mkdir
from pdpp.utils.yaml_task import dump_self
from pdpp.templates.dep_dataclass import dep_dataclass
from pdpp.utils.execute_at_target import execute_at_target


class ExportTask(BasePDPPClass):
    """
    This is the class documentation
    """

    def __init__(
            self
            ):

        self.target_dir: str = "_export_"
        self.dep_files: Dict[str, dep_dataclass] = {}
        self.enabled: bool = True
        self.src_files: List = []


    FILENAME = ".pdpp_export.yaml"
    RIG_VALID = True # Can be rigged
    TRG_VALID = False # Can have targets 
    DEP_VALID = False # Can contain dependencies for other tasks
    SRC_VALID = False # Can have source code
    RUN_VALID = False # Has actions that should be executed at runtime
    IN_DIR = "./"
    OUT_DIR = "./"
    SRC_DIR = False

    def provide_run_actions(self) -> Tuple:
        return ()

    def provide_src_dependencies(self) -> List:
        return []

    def rig_task(self):
        from pdpp.utils.directory_test import get_dependency_tasks
        from pdpp.questions import q1, q2, q3, q4
        from pdpp.utils.immediate_link import immediate_link

        # Ask dependency questions:
        dep_tasks = get_dependency_tasks()
        selected_dep_tasks = q1(dep_tasks, self)
        self.dep_files = q2(selected_dep_tasks, self)

        # Implement links:
        # TODO: Consider creating a check for files that aren't part of the
        # existing dependency structure; if there are any, ask if users want
        # them deleted or to be preserved.
        immediate_link(self)

        # Finally, save self to YAML:
        #execute_at_target(dump_self, self)
        self.save_self()

    def initialize_task(self):
        mkdir(self.target_dir)
        execute_at_target(dump_self, self)

    def provide_dependencies(self, asking_task: BasePDPPClass) -> List[str]:
        try:
            return self.dep_files[asking_task.target_dir].compile_targets()
        except KeyError:
            pass

        return []