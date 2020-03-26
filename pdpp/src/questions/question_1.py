import questionary
from questionary import Separator, Choice, prompt
from click import clear as click_clear

def q1(subdirs, target_dir, yaml_dict, custom_style_fancy):

    click_clear()

    choice_list = []

    for directory in subdirs:
        if directory == target_dir:
            choice_list.append({
                'name': directory,
                'disabled': "This is the selected step"
            })
        else:
            choice_list.append({
                'name': directory,
                'checked': directory in yaml_dict,
                })


    questions_1 = [
        {
            'type': 'checkbox',
            'message': 'Select steps which contain dependencies for "{}"'.format(target_dir),
            'name': 'dep_steps',
            'choices': choice_list,
        }
    ]


    try:
        return prompt(questions_1, style=custom_style_fancy)['dep_steps']
    except IndexError:
        return
