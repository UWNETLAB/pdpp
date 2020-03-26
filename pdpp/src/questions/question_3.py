import questionary
from questionary import Separator, Choice, prompt
from click import clear as click_clear
from os.path import isdir
from os import listdir, walk
from posixpath import join

def q3(target_dir, yaml_dict, custom_style_fancy):

    click_clear()

    source_files = []

    for root, dirs, files in walk(join(target_dir, 'src')):
        for script in files: 
            if script != '.gitkeep':
                source_files.append({
                    'name': script,
                    'checked': script in yaml_dict,
                })  


    question_3 = [{
            'type': 'checkbox',
            'message': 'Select the source files for "{}"'.format(target_dir),
            'name': 'source',
            'choices': source_files,
        }]

    try:
        return prompt(question_3, style=custom_style_fancy)['source']
    except IndexError:
        return []
    except AssertionError:
        return []

        
    
    
