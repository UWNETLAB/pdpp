import os
from posixpath import join
from typing import List

from pdpp.automation.mylinker import dir_linker, file_linker
from pdpp.tasks.base_task import BaseTask


def make_link_task(task: BaseTask, disabled_list: List[str], final_dep_list: List):
    for task_with_dependency, dependency_metadata in task.dep_files.items():
        link_action_list = []
        link_dep_list = []
        link_targ_list = []

        if task_with_dependency not in disabled_list:
            file_link_start = [
                join(task_with_dependency, dependency_metadata.task_out, f)
                for f in dependency_metadata.file_list
            ]
            file_link_end = [
                join(task.target_dir, task.IN_DIR, f)
                for f in dependency_metadata.file_list
            ]

            link_action_list.extend(
                [
                    (file_linker, [fls, fle])
                    for fls, fle in list(zip(file_link_start, file_link_end))
                ]
            )

            dir_link_start = [
                join(task_with_dependency, dependency_metadata.task_out, f)
                for f in dependency_metadata.dir_list
            ]
            dir_link_end = [
                join(task.target_dir, task.IN_DIR, f)
                for f in dependency_metadata.dir_list
            ]

            link_action_list.extend(
                [
                    (dir_linker, [dls, dle])
                    for dls, dle in list(zip(dir_link_start, dir_link_end))
                ]
            )

            link_dep_list.extend(file_link_start)
            link_targ_list.extend(file_link_end)

            for dir_dependency in dependency_metadata.dir_list:
                path_to_dep_dir = join(
                    dependency_metadata.task_name, dependency_metadata.task_out
                )
                startdir = os.getcwd()
                os.chdir(path_to_dep_dir)
                for root, _, filenames in os.walk(dir_dependency):
                    for filename in filenames:
                        subdir_filepath_start = join(
                            dependency_metadata.task_name,
                            dependency_metadata.task_out,
                            root,
                            filename,
                        )
                        link_dep_list.append(subdir_filepath_start)

                        subdir_filepath_end = join(
                            task.target_dir, task.IN_DIR, root, filename
                        )
                        link_targ_list.append(subdir_filepath_end)
                os.chdir(startdir)

            final_dep_list.extend(link_targ_list)

            yield {
                "basename": "_task_{}_LINK_TO_{}".format(
                    task_with_dependency, task.target_dir
                ),
                "actions": link_action_list,
                "file_dep": link_dep_list,
                "targets": link_targ_list,
                "clean": True,
            }
