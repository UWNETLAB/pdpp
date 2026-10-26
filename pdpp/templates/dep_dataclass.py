from dataclasses import dataclass
from posixpath import join


@dataclass
class dep_dataclass:
    task_out: str
    task_name: str
    file_list: list[str]
    dir_list: list[str]

    def compile_targets(self):
        files: list[str] = [
            join(self.task_name, self.task_out, f) for f in self.file_list
        ]
        dirs: list[str] = [
            join(self.task_name, self.task_out, f) for f in self.dir_list
        ]

        full_list = [*files, *dirs]

        return full_list
