from os import link, remove, walk
from posixpath import join
from shutil import copytree, rmtree

from pdpp.tasks.base_task import BaseTask
from pdpp.utils.ignorelist import ignorelist


def immediate_link(task: BaseTask):
    """
    This is a docstring.
    """

    # The following block cleans the input directory by deleting everything
    # in it recursively, except for things on the ignorelist

    in_dir = join(task.target_dir, task.IN_DIR)
    for root, dirs, files in walk(in_dir):
        for name in [f for f in files if f not in ignorelist]:
            remove(join(in_dir, name))
        for name in dirs:
            rmtree(join(in_dir, name))

    for key, value in task.dep_files.items():
        out_dir = join(key, value.task_out)

        for file_entry in value.file_list:
            pre_link = join(out_dir, file_entry)
            post_link = join(in_dir, file_entry)
            link(pre_link, post_link)

        for directory_entry in value.dir_list:
            pre_link = join(out_dir, directory_entry)
            post_link = join(in_dir, directory_entry)
            copytree(pre_link, post_link, copy_function=link)
