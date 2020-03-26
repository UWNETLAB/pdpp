import questionary
from questionary import Separator, Choice, prompt
from click import clear as click_clear
from os.path import isdir
from os import listdir, walk
from posixpath import join

def q5(target_dir, custom_style_fancy):


    click_clear()

    question_5 = [
        {
            'type': 'list',
            'name': 'target_status',
            'message': "Are the step's targets ready to be rigged?", 
            'choices': [
                {
                    'name': 'Yes',
                    'value': True,
                },
                {
                    'name': 'No',
                    'value': False,
                }
                
            ]
        }
    ]

    try:
        return prompt(question_5, style=custom_style_fancy)['target_status']
    except IndexError:
        return []
    except AssertionError:
        return []
    