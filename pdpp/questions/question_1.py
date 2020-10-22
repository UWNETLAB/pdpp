from questionary import prompt, Choice
from click import clear as click_clear
from pdpp.styles.prompt_style import custom_style_fancy 
from pdpp.pdpp_class_base import BasePDPPClass
from typing import List




def q1(dep_tasks: List[BasePDPPClass], task: BasePDPPClass) -> List[BasePDPPClass]:
    """
    This question is used to determine which other steps in the project structure are dependencies of the current step. 
    """

    click_clear()

    choice_list = []

    '''
    First, add all the project subdirectories (riggable_subdirectories) returned from Question 0. 
    When this process encounters the step being rigged (target_dir), add it to the list as a disabled entry. 
    '''

    for dep_task in dep_tasks:
        if dep_task.target_dir == task.target_dir:
            choice_list.append(
                Choice(
                    title=dep_task.target_dir,
                    value=dep_task,
                    disabled='This is the selected step'
                )
            )

        else:
            choice_list.append(
                Choice(
                    title=dep_task.target_dir,
                    value=dep_task,
                    checked=dep_task.target_dir in task.dep_files
                )
            )
            
    if len(choice_list) < 1:
        return []

    questions_1 = [
        {
            'type': 'checkbox',
            'message': 'Select steps which contain dependencies for "{}"'.format(task.target_dir),
            'name': 'dep_steps',
            'choices': choice_list,
        }
    ]

    return prompt(questions_1, style=custom_style_fancy)['dep_steps']