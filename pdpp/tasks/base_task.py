from typing import Dict, List

from pdpp.languages.language_enum import Language
from pdpp.templates.dep_dataclass import dep_dataclass
from pdpp.utils.execute_at_target import execute_at_target
from pdpp.utils.yaml_task import dump_self


class BaseTask:
    """
    This is a docstring.
    """

    def __init__(self, target_dir):
        self.target_dir: str
        self.dep_files: Dict[str, dep_dataclass]
        self.src_files: List
        self.language: str = Language.NULL.value
        self.enabled: bool

    FILENAME = ".pdpp_task.yaml"
    RIG_VALID = True  # Can be rigged
    TRG_VALID = False  # Can have targets
    DEP_VALID = True  # Can contain dependencies for other tasks
    SRC_VALID = False  # Should soucre code be automatically parsed?
    RUN_VALID = True  # Has actions that should be executed at runtime
    IN_DIR: str
    OUT_DIR: str
    SRC_DIR: str

    def provide_run_actions(self) -> List:
        return []

    def provide_src_dependencies(self) -> List:
        return []

    def provide_dependencies(self, asking_task) -> List[str]:
        try:
            return self.dep_files[asking_task.target_dir].compile_targets()
        except KeyError:
            return []

    def rig_task(self):
        from pdpp.questions import q1, q2, q3, q4
        from pdpp.utils.directory_test import get_dependency_tasks
        from pdpp.utils.immediate_link import immediate_link

        # Ask dependency questions:
        dep_tasks = get_dependency_tasks()
        selected_dep_tasks = q1(dep_tasks, self)
        self.dep_files = q2(selected_dep_tasks, self)

        # Ensure source compliance:
        if self.SRC_VALID:
            self.src_files = q3(self)
            self.language = q4(self)

        # Implement links:
        # TODO: Consider creating a check for files that aren't part of the
        # existing dependency structure; if there are any, ask if users want
        # them deleted or to be preserved.
        immediate_link(self)

        # Finally, save self to YAML:
        # execute_at_target(dump_self, self)
        self.save_self()

    def initialize_task(self):
        raise NotImplementedError

    def save_self(self):
        execute_at_target(dump_self, self)

    def enable(self):
        self.enabled = True
        self.save_self()

    def disable(self):
        self.enabled = False
        self.save_self()
