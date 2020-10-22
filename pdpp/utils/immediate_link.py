from os import link, makedirs
from posixpath import join
from typing import List
from pdpp.pdpp_class_base import BasePDPPClass
from shutil import rmtree, copytree


def immediate_link(task:BasePDPPClass):
    """
    This is a docstring.
    """

    #The following block cleans the input directory by deleting it recursively
    #and then re-creating it with a new .gitkeep

    in_dir = join(task.target_dir, task.IN_DIR)
    rmtree(in_dir)
    makedirs(in_dir)
    with open(join(in_dir, ".gitkeep"), 'w'):
        pass

    for key, value in task.dep_files.items():
        
        out_dir = join(key, value["task_out"])

        for file_entry in value['file_list']:
            pre_link = join(out_dir, file_entry)
            post_link = join(in_dir, file_entry)
            link(pre_link, post_link)
        
        for directory_entry in value['dir_list']:
            pre_link = join(out_dir, directory_entry)
            post_link = join(in_dir, directory_entry)
            copytree(pre_link, post_link, copy_function=link)