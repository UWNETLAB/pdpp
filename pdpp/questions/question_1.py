from questionary import prompt
from click import clear as click_clear
from pdpp.styles.prompt_style import custom_style_fancy 
from pdpp.pdpp_class import step_class
from typing import List


def q1(subdirs: list, target_dir: str, step_metadata: step_class) -> List[str]:
    """
    This question is used to determine which other steps in the project structure are dependencies of the current step. 
    """

    click_clear()

    choice_list = []

    if target_dir == "_export_":
        subdirs.remove("_import_")

    if "_export_" in subdirs:
        subdirs.remove("_export_")

    '''
    First, add all the project subdirectories (subdirs) returned from Question 0. When this process encounters the step being rigged (target_dir), add it to the list as a disabled entry. 
    '''

    for directory in subdirs:
        if directory == target_dir:
            choice_list.append({
                'name': directory,
                'disabled': "This is the selected step"
            })
        elif directory == "_import_":
            choice_list.append({
                'name': '_import_',
                'checked': len(step_metadata.import_files) > 0
            })
        else:
            choice_list.append({
                'name': directory,
                'checked': directory in step_metadata.dep_files,
                })

    if len(choice_list) < 1:
        return []

    questions_1 = [
        {
            'type': 'checkbox',
            'message': 'Select steps which contain dependencies for "{}"'.format(step_metadata.target_dir),
            'name': 'dep_steps',
            'choices': choice_list,
        }
    ]

    return prompt(questions_1, style=custom_style_fancy)['dep_steps']