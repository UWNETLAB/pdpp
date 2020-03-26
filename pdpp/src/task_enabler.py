from os import scandir
from pdpp.src.utils.proj_folder_test import proj_folder_test
from posixpath import join, exists
from pdpp.src.yaml_handlers.import_yaml import import_yaml
from pdpp.src.styles.prompt_style import custom_style_fancy 
from click import clear as click_clear
from questionary import Separator, Choice, prompt
from pprint import pprint
import yaml

def task_enabler():

    subdirs= [f.path.replace('./', '').replace('.\\', '') for f in scandir() if proj_folder_test(f)]

    yaml_steps = []

    for directory in subdirs:
        if exists(join(directory, "pdpp_step.yaml")):
            yaml_step, junk = import_yaml(directory, return_empty=False)
            yaml_steps.append(yaml_step)

    click_clear()

    choice_list = []

    for step in yaml_steps:
        choice_list.append({
            'name': step['target_dir'],
            'checked': step['enabled'],
            })


    questions_1 = [
        {
            'type': 'checkbox',
            'message': "Select the steps which will be run when 'pdpp run' is called",
            'name': 'enabled',
            'choices': choice_list,
        }
    ]

    try:
        enabled_list = prompt(questions_1, style=custom_style_fancy)['enabled']
    except IndexError:
        print('There are no valid steps in this project directory!')
    
    for step in yaml_steps:

        yaml_loc = join(step['target_dir'], 'pdpp_step.yaml')

        if step['target_dir'] in enabled_list:
            step['enabled'] = True
        else:
            step['enabled'] = False

        pprint(step)

        with open(yaml_loc, 'w') as stream:
            yaml.dump(step, stream, default_flow_style=False)


    

    