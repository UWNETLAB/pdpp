from pdpp.utils.directory_test import get_pdpp_directories
from posixpath import join, exists
from pdpp.styles.prompt_style import custom_style_fancy 
from questionary import prompt
import yaml
from pdpp.pdpp_class_base import BasePDPPClass
from pdpp.task_types import all_task_types
 
def task_enabler():

    subdirs, _ = get_pdpp_directories()

    pdpp_steps = []

    for directory in subdirs:
        for pdpp_class in all_task_types:
            if exists(join(directory, pdpp_class.FILENAME)):
                pdpp_steps.append(import_step_class(directory, pdpp_class.FILENAME))

    choice_list = []

    for step in pdpp_steps:
        choice_list.append({
            'name': step.target_dir,
            'checked': step.enabled,
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
        enabled_list = []
    
    for step in pdpp_steps:

        yaml_loc = join(step.target_dir, step.filename)

        if step.target_dir in enabled_list:
            step.enabled = True
        else:
            step.enabled = False

        with open(yaml_loc, 'w') as stream:
            yaml.dump(step, stream, default_flow_style=False)


    

    