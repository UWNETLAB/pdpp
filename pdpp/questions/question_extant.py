from questionary import prompt, Choice
from click import clear as click_clear
from pdpp.styles.prompt_style import custom_style_fancy 
from pdpp.utils.directory_test import get_pdpp_tasks
from pdpp.tasks.standard_task import StandardTask
import os


def q_extant() -> StandardTask:
    '''
    This question is used to select the directory you wish to automate.
    '''

    task_dirs = [d.target_dir for d in get_pdpp_tasks()]

    

    click_clear()

    dir_list = [d.name for d in os.scandir() if d.name not in task_dirs and d.is_dir()]

    choice_list = []

    print(task_dirs)
    print(dir_list)

    for _dir in dir_list:
        choice_list.append(
            Choice(
                title=_dir,
                value=_dir,
            )
        )


    questions_0 = [
        {
            'type': 'list',
            'name': 'target_dir',
            'message': 'Select the directory you would like to automate:', 
            'choices': choice_list
        }
    ]

    dirname = prompt(questions_0, style=custom_style_fancy)['target_dir']
    
    
    return StandardTask(target_dir = dirname)
