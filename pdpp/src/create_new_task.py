import os
from pdpp.src.questions.question_1 import q1
from pdpp.src.questions.question_2 import q2
from pdpp.src.yaml_handlers.import_yaml import import_yaml
from os import scandir, link
from pdpp.src.utils.proj_folder_test import proj_folder_test
from pprint import pprint 
import yaml
from prompt_toolkit.styles import Style
from pdpp.src.utils.immediate_link import immediate_link
from pdpp.src.styles.prompt_style import custom_style_fancy

def create_new_task(dirname):

    dirname = dirname.lower()

    try:
        f = open("dodo.py", "x")
        f.write(
"""from pdpp.src.task_creator import gen_many_tasks, task_all

import doit
doit.run(globals())
"""
)
        f.close()
    except FileExistsError:
        pass

    try:
        f = open(".gitignore", "x")
        f.write(
""".*!/.gitignore!.gitkeep__pycache__.pyc
/.*
!/.gitignore
*__pycache__
.ipynb_checkpoints
__pycache__
*.pyc
/dist/
/venv/
/build/
/*.egg-info
/*.egg
/.idea
*.db
*.bak
*.dat
*.dir""")
    except FileExistsError:
        pass

    os.makedirs(os.path.join(dirname, "input"))
    os.makedirs(os.path.join(dirname, "output"))
    os.makedirs(os.path.join(dirname, "src"))
    
    f = open(os.path.join(dirname, "input", ".gitkeep"), "a")
    f.close()

    f = open(os.path.join(dirname, "output", ".gitkeep"), "a")
    f.close()

    f = open(os.path.join(dirname, "src", ".gitkeep"), "a")
    f.close()

    f = open(os.path.join(dirname, "src", (dirname + ".py")), "a")
    f.close()

    yaml_dict, yaml_loc = import_yaml(dirname)

    subdirs= [f.path.replace('./', '').replace('.\\', '') for f in scandir() if proj_folder_test(f)]

    # Question 1 - Which other Steps contain necessary dependencies?
    dep_dirs = q1(subdirs, dirname, yaml_dict['dep_dirs'], custom_style_fancy)

    # Question 2 - Which files from the indicated dependencies are needed?
    if len(dep_dirs) != 0 and dep_dirs != None:
        dep_files, dep_dirs = q2(dep_dirs, dirname, yaml_dict['dep_files'], custom_style_fancy)
    else:
        dep_files = []
        dep_dirs = []
    
    immediate_link(dep_files)

    step_dict = {
    'target_dir': dirname,
    'dep_dirs': dep_dirs,
    'dep_files': dep_files,
    'src_files': yaml_dict['src_files'],
    'language': yaml_dict['language'],
    'target_status': yaml_dict['target_status'],
    'target_files': yaml_dict['target_files'],
    'self_deps': yaml_dict['self_deps'],
    'enabled': yaml_dict['enabled']
    }

    pprint(step_dict)

    with open(yaml_loc, 'w') as stream:
        yaml.dump(step_dict, stream, default_flow_style=False)
