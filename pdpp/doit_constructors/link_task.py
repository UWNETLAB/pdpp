from pdpp.pdpp_class_base import BasePDPPClass
from pdpp.doit_constructors.mylinker import file_linker, dir_linker
from typing import List
from posixpath import join


def make_link_task(task: BasePDPPClass, disabled_list: List[str]):

    for task_with_dependency, dependency_metadata in task.dep_files.items():

        link_action_list = [] 
        link_dep_list = []
        link_targ_list = []

        if task_with_dependency not in disabled_list: 

            file_link_start = [join(task_with_dependency, dependency_metadata.task_out, f) for f in dependency_metadata.file_list]
            file_link_end = [join(task.target_dir, task.IN_DIR, f) for f in dependency_metadata.file_list]

            link_action_list.extend([(file_linker, [fls, fle]) for fls, fle in list(zip(file_link_start, file_link_end))])

            dir_link_start = [join(task_with_dependency, dependency_metadata.task_out, f) for f in dependency_metadata.dir_list]
            dir_link_end = [join(task.target_dir, task.IN_DIR, f) for f in dependency_metadata.dir_list]

            link_action_list.extend([(dir_linker, [dls, dle]) for dls, dle in list(zip(dir_link_start, dir_link_end))])

            yield {
                'basename': '_task_{}_LINK_TO_{}'.format(task_with_dependency, task.target_dir),
                'actions': link_action_list,
                'file_dep': link_dep_list,
                'targets': link_targ_list,
                'clean': True,
            }