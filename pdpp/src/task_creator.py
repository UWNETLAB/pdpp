from os import scandir, getcwd
from os.path import isdir
from posixpath import join, exists
from pdpp.src.yaml_handlers.import_yaml import import_yaml
from pdpp.src.doit_constructors.link_task import make_link_task
from pprint import pprint
from pathlib import Path
from pdpp.src.doit_constructors.mylinker import mylinker
from importlib import import_module
from pdpp.src.languages.python_runner import python_runner
from pdpp.src.languages.r_runner import r_runner
from pdpp.src.utils.proj_folder_test import proj_folder_test
#from pdpp.src.questions.question_6 import q6

 
def gen_many_tasks():
     
    subdirs= [f.path.replace('./', '').replace('.\\', '') for f in scandir() if proj_folder_test(f)]

    yaml_steps = []

    for directory in subdirs:
        if exists(join(directory, "pdpp_step.yaml")):
            yaml_step, junk = import_yaml(directory, return_empty=False)
            yaml_steps.append(yaml_step)

    disabled_list = []

    target_unrigged = False
    target_unrigged_list = []


    for step in yaml_steps:
        if step['enabled'] == False:
            disabled_list.append(step['target_dir'])

        elif step['target_status'] == False:
            print(f"""
        The '{step['target_dir']}' step is enabled, 
        but has not yet had its targets rigged.            """)
            target_unrigged = True
            target_unrigged_list.append(step['target_dir'])


    if target_unrigged:
        print("""
        Please use pdpp rig to enable and configure
        the targets for each of the following steps:""")
        print(f"""
        {target_unrigged_list}""" )
        quit()


    for step in yaml_steps:
        if step['enabled'] == False:
            pass

        else:
            dep_list = []

            for source_file in step['src_files']:
                dep_list.append(join(step['target_dir'], 'src', source_file))
                
            for self_dep in step['self_deps']:
                dep_list.append(self_dep)
            
            targ_list = step['target_files']
            action_list = []

            if step['language'] == "Python":
                runner = python_runner
            elif step['language'] == "R":
                runner = r_runner

            yield make_link_task(step, dep_list, disabled_list, mylinker)
            
            for source_file in step['src_files']:
                action_list.append((runner, [source_file, step['target_dir']], {}))

            yield {
                'basename': '{}'.format(step['target_dir']),
                'actions': action_list,
                'file_dep': dep_list,
                'targets': targ_list,
                'clean': True,
            }



def task_all():
    yield gen_many_tasks()

if __name__ == '__main__':
    import doit
    doit.run(globals())