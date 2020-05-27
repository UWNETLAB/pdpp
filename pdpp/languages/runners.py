from os import name
from subprocess import run
from posixpath import join

def python_runner(script_name, target_dir):
    if name == 'posix':
        python_caller = 'python3'
    else:
        python_caller = 'python'
    run([python_caller, script_name], check=True, cwd=join(target_dir, 'src'))

def r_runner(script_name, target_dir):
    run(['Rscript', script_name], check=True, cwd=join(target_dir, 'src'))

def project_runner(target_dir: str):
    run(["doit"], check=True, cwd=target_dir)