from pdpp.pdpp_class_base import BasePDPPClass
from typing import List, Tuple, Dict
from os import mkdir
from posixpath import join
from pdpp.utils.execute_at_target import execute_at_target
from pdpp.templates.create_in_out_src import create_in_out_src
from pdpp.utils.yaml_task import dump_self
from pdpp.languages.language_enum import Language
from pdpp.templates.dep_dataclass import dep_dataclass
from pdpp.languages.language_parser import parse_language
from pdpp.languages.runners import project_runner


class StepTask(BasePDPPClass):
    """
    This is the class documentation
    """

    def __init__(
            self,
            target_dir
            ):

        self.target_dir = target_dir
        self.dep_files: Dict[str, dep_dataclass] = {}
        self.src_files: List = []
        self.language: str = Language.PYTHON.value
        self.enabled: bool = True


    # region
    FILENAME = ".pdpp_step.yaml"
    RIG_VALID = True # Can be rigged
    TRG_VALID = True # Can have targets 
    DEP_VALID = True # Can contain dependencies for other tasks
    SRC_VALID = True # Can have source code
    RUN_VALID = True # Has actions that should be executed at runtime
    IN_DIR = "input"
    OUT_DIR = "output"
    SRC_DIR = "src"
    # endregion


    def provide_run_actions(self):
        runner = parse_language(self)
        
        return tuple((runner, [s, self], {}) for s in self.src_files)

    def provide_src_dependencies(self) -> List:
        return [join(self.target_dir, self.SRC_DIR, s) for s in self.src_files]


    def rig_task(self):

        from pdpp.utils.directory_test import get_dependency_tasks
        from pdpp.questions import q1, q2, q3, q4
        from pdpp.utils.immediate_link import immediate_link

        # Ask dependency questions:
        dep_tasks = get_dependency_tasks()
        selected_dep_tasks = q1(dep_tasks, self)
        self.dep_files = q2(selected_dep_tasks, self)

        # Ensure source compliance:
        self.src_files = q3(self)
        self.language = q4(self)

        # Implement links:
        # TODO: Consider creating a check for files that aren't part of the
        # existing dependency structure; if there are any, ask if users want
        # them deleted or to be preserved.
        immediate_link(self)

        # Finally, save self to YAML:
        #execute_at_target(dump_self, self)
        self.save_self()


    def initialize_task(self):

        # Create directory structure:
        mkdir(self.target_dir)
        execute_at_target(create_in_out_src, self)

        # From here on out, rigging is identical to creating anew:
        self.rig_task()


    def provide_dependencies(self, asking_task: BasePDPPClass) -> List[str]:
        # The 'asking_task' can be thought of as the one asking which of its files are needed
        # by this ('self') task.
        try:
            return self.dep_files[asking_task.target_dir].compile_targets()
        except KeyError:
            pass

        return []

