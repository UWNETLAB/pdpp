from os import name
from posixpath import join
from subprocess import run

from pdpp.tasks.base_task import BaseTask


def python_runner(script_name: str, task: BaseTask):
    if name == "posix":
        python_caller = "python3"
    else:
        python_caller = "python"
    run(
        [python_caller, script_name],
        check=True,
        cwd=join(task.target_dir, task.SRC_DIR),
    )


def r_runner(script_name, target_dir, src_dir):
    run(["Rscript", script_name], check=True, cwd=join(target_dir, src_dir))


# TODO: Fix the project runner and bring it in line with the other runners
def project_runner(task: BaseTask):
    run(["doit"], check=True, cwd=task.target_dir)
