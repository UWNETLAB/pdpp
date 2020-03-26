from os import chdir, name
from subprocess import run

def r_runner(script_name, target_dir):
    chdir(target_dir)
    chdir('src')
    run(['Rscript', script_name], check=True)
    chdir('..')
    chdir('..')