from pdpp.utils.directory_test import get_riggable_directories
from posixpath import join, exists
from pdpp.styles.prompt_style import custom_style_fancy 
from questionary import prompt
import yaml
from pdpp.utils.import_step_class import import_step_class
from pdpp.pdpp_class import step_class, export_class, project_class, custom_class
 
def task_enabler():

    subdirs = get_riggable_directories()

    classes_to_load = [step_class, export_class, project_class, custom_class]

    pdpp_steps = []

    for directory in subdirs:
        for pdpp_class in classes_to_load:
            if exists(join(directory, pdpp_class.filename)):
                pdpp_steps.append(import_step_class(directory, pdpp_class.filename))

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


    

    