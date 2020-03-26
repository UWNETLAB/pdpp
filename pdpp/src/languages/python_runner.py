from os import chdir, name
from subprocess import run

def python_runner(script_name, target_dir):
    chdir(target_dir)
    chdir('src')
    if name == 'posix':
        python_caller = 'python3'
    else:
        python_caller = 'python'
    run([python_caller, script_name], check=True)
    chdir('..')
    chdir('..')