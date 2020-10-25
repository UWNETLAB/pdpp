from dataclasses import dataclass
from typing import List
from posixpath import join 

@dataclass
class dep_dataclass():
    task_out: str
    task_name: str
    file_list: List[str]
    dir_list: List[str]

    def compile_targets(self):
        files: List[str] = [join(self.task_name, self.task_out, f) for f in self.file_list]
        dirs: List[str]  = [join(self.task_name, self.task_out, f) for f in self.dir_list]

        full_list = [*files, *dirs]
                
        return full_list

