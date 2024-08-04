from os import link, remove
from shutil import copytree, rmtree


def file_linker(link_start, link_end):
    try:
        link(link_start, link_end)
    except FileExistsError:
        remove(link_end)
        link(link_start, link_end)


def dir_linker(link_start, link_end):
    try:
        copytree(link_start, link_end, copy_function=link)
    except FileExistsError:
        rmtree(link_end)
        copytree(link_start, link_end, copy_function=link)
