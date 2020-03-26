import questionary
from questionary import Separator, Choice, prompt
from click import clear as click_clear
from os.path import isdir
from os import scandir

def q0(proj_folder_test, custom_style_fancy):

    subdirs= [f.path.replace('./', '').replace('.\\', '') for f in scandir() if proj_folder_test(f)]

    subdirs.sort()

    click_clear()

    questions_0 = [
        {
            'type': 'list',
            'name': 'target_dir',
            'message': 'select target step', 
            'choices': subdirs
        }
    ]

    click_clear()

    try:
        return prompt(questions_0, style=custom_style_fancy)['target_dir'], subdirs
    except IndexError:
        return []
    except AssertionError:
        return []
