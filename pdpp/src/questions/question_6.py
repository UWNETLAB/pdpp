import questionary
from questionary import Separator, Choice, prompt
from click import clear as click_clear
from os.path import isdir
from os import listdir, walk
from posixpath import join

def q6(target_dir, yaml_dict, custom_style_fancy):


    click_clear()

    target_files = []

    for root, dirs, files in walk(join(target_dir, 'output')):
        for outputs in files: 
            if outputs != '.gitkeep':
                specific_root = root.replace('./', '').replace('.\\', '')
                target_files.append({
                    'name': join(specific_root, outputs),
                    'checked': join(specific_root, outputs) in yaml_dict,
                }) 


    question_6 = [{
            'type': 'checkbox',
            'message': 'Select the targets for the "{}" step'.format(target_dir),
            'name': 'targets',
            'choices': target_files,
        }]

    try:
        return prompt(question_6, style=custom_style_fancy)['targets']
    except IndexError:
        return []
    except AssertionError:
        return []
    