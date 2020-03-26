import questionary
from questionary import Separator, Choice, prompt
from click import clear as click_clear
from os.path import isdir
from posixpath import join
import os
from pprint import pprint

def q2(output_dirs, target_dir, yaml_dict, custom_style_fancy):

    click_clear()

    q2input = {}

    for directory in output_dirs:
        q2input[directory] = []
        for root, dirs, files in os.walk(join(directory, 'output')):
            root = root.replace('\\', '/').replace('./', '').replace('.\\', '')
            for entry in files:
                if entry != '.gitkeep':
                    output = join(root, entry).replace('./', '')
                    q2input[directory].append(output) 

    choice_list_2 = []

    for key in q2input:
        choice_list_2.append(Separator('\n= ' + key + ' ='))
        for value in q2input[key]:
            try:
                checked = value in yaml_dict[key]
            except KeyError:
                checked = False
            choice_list_2.append({
                'name': join(value),
                'checked': checked,
                })

    questions_2 =[
        {
            'type': 'checkbox',
            'message': 'Select the dependency files for "{}"'.format(target_dir),
            'name': 'dependencies',
            'choices': choice_list_2,
        }
    ]
    
    try:
        responses = prompt(questions_2, style=custom_style_fancy)['dependencies']
    except IndexError:
        return {}
    except AssertionError:
        return {}

    response_dict={}


    for dep_dir in output_dirs:

        response_dict[dep_dir] = {}

        for response in responses:
            if join(dep_dir, 'output') in response:
                response_dict[dep_dir][response] = {
                    'pre_link': response,
                    'post_link': join(target_dir, 'input', response.split('output/')[-1]),
                    }

        if len(response_dict[dep_dir]) == 0:
            del response_dict[dep_dir]
            output_dirs.remove(dep_dir)

        # dep_linked_files = {}

        # for key in response_dict:
        #     dep_linked_files[key] = []
        #     for entry in response_dict[key]:
        #         dep_linked_files[key].append(join(target_dir, 'input', entry.split('/')[-1]))


    
    pprint(response_dict)


    return response_dict, output_dirs