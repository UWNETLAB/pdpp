from os import makedirs
from posixpath import join

from pdpp.tasks.base_task import BaseTask


def create_in_out_src(task: BaseTask):
    """
    Creates the input, output, and src directories, as well as a source file and
    .gitkeep files, in the new task.
    """

    makedirs("input")
    makedirs("output")
    makedirs("src")

    open(join("input", ".gitkeep"), "a").close()
    open(join("output", ".gitkeep"), "a").close()
    open(join("src", ".gitkeep"), "a").close()
    open(join("src", (task.target_dir + ".py")), "a").close()
