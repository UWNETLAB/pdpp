import questionary
from questionary import Separator, Choice, prompt
from click import clear as click_clear
from os.path import isdir
from posixpath import join
from os import listdir, scandir, walk

def q2_A(target_dir, yaml_dict, dep_files, custom_style_fancy):

    click_clear()

    choice_list_2_A = []

    self_files = []

    for root, dirs, files in walk(join(target_dir, 'input')):
        root = root.replace('\\', '/').replace('./', '').replace('.\\', '')
        for entry in files:
            if entry != '.gitkeep':
                self_files.append(join(root, entry).replace('./', ''))
                


    #rawinputs = [f.path.replace('./', '').replace('.\\', '').replace('\\','/').split('/')[-1] for f in scandir(join(target_dir, 'input'))]

    inputs = []

    dep_file_list = []

    for source in dep_files:
        for entry in dep_files[source]:
            dep_file_list.append(dep_files[source][entry]['post_link'].split('/')[-1])

    print(dep_file_list)

    for entry in self_files:
        if '.gitkeep' in entry or entry.split('/')[-1] in dep_file_list:
            pass
        else:
            inputs.append(entry)


    choice_list_2_A.append(Separator('\n= ' + target_dir + ' ='))

    for entry in inputs:
        try:
            checked = entry in yaml_dict
        except KeyError:
            checked = False
        choice_list_2_A.append({
            'name': entry,
            'checked': checked,
            })

    questions_2_A =[
        {
            'type': 'checkbox',
            'message': 'Select dependency files which DO NOT originate from another step in the workflow',
            'name': 'dependencies',
            'choices': choice_list_2_A,
        }
    ]
    
    if len(inputs) == 0:
        return []

    try:
        self_deps = prompt(questions_2_A, style=custom_style_fancy)['dependencies']
    except IndexError:
        return []
    except AssertionError:
        return []

    return self_deps