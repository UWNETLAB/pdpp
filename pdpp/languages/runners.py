from os import name
from subprocess import run
from posixpath import join
from pdpp.pdpp_class_base import BasePDPPClass

def python_runner(script_name: str, task: BasePDPPClass):
    if name == 'posix':
        python_caller = 'python3'
    else:
        python_caller = 'python'
    run([python_caller, script_name], check=True, cwd=join(task.target_dir, task.SRC_DIR))

def r_runner(script_name, target_dir, src_dir):
    run(['Rscript', script_name], check=True, cwd=join(target_dir, src_dir))

# TODO: Fix the project runner and bring it in line with the other runners
def project_runner(target_dir: str):
    run(["doit"], check=True, cwd=target_dir)