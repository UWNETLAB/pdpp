from os import link, remove, makedirs
from posixpath import join
from typing import List
from pdpp.pdpp_class import base_pdpp_class


def immediate_import_link(this_class:base_pdpp_class):
    """
    This is a docstring.
    """

    for import_file in this_class.import_files:

        pre_link = join("_import_", import_file)
        post_link = join(this_class.target_dir, this_class.in_dir, import_file)

        try:
            link(pre_link, post_link)
        except FileExistsError:
            remove(post_link)
            link(pre_link, post_link)
        except FileNotFoundError:
            post_link_list = post_link.split('/')
            del post_link_list[-1]

            if len(post_link_list) != 0:
                makedirs(join(*post_link_list))

            link(pre_link, post_link)


def immediate_link(this_class:base_pdpp_class, riggables: List[base_pdpp_class]):
    """
    This is a docstring.
    """

    for dep_step in this_class.dep_files:

        dep_files = this_class.dep_files[dep_step]

        dep_class = next((c for c in riggables if c.target_dir == dep_step))

        for dep_file in dep_files:

            pre_link = join(dep_class.target_dir, dep_class.out_dir, dep_file)
            post_link = join(this_class.target_dir, this_class.in_dir, dep_file)

            try:
                link(pre_link, post_link)
            except FileExistsError:
                remove(post_link)
                link(pre_link, post_link)
            except FileNotFoundError:
                post_link_list = post_link.split('/')
                del post_link_list[-1]

                if len(post_link_list) != 0:
                    makedirs(join(*post_link_list))

                link(pre_link, post_link)