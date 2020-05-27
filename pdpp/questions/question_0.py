from questionary import prompt
from click import clear as click_clear
from posixpath import  exists, join
from pdpp.styles.prompt_style import custom_style_fancy 
from pdpp.utils.directory_test import get_riggable_directories
from pdpp.pdpp_class import step_class, custom_class, project_class, export_class, base_pdpp_class
from typing import Tuple

def q0() -> Tuple[str, base_pdpp_class, dict] :
    '''
    This question is used to select the step you wish to alter with pdpp.
    '''

    subdirs = get_riggable_directories()
    subdirs.sort()

    click_clear()


    questions_0 = [
        {
            'type': 'list',
            'name': 'target_dir',
            'message': 'Select the step you would like to rig', 
            'choices': subdirs
        }
    ]
    
    click_clear()

    target_dir = str(prompt(questions_0, style=custom_style_fancy)['target_dir'])

    subdirs.remove("_export_")

    subdirs.append("_import_")

    subdirs.sort()

    class_list = [step_class, custom_class, project_class, export_class]

    target_dir_class = None

    for _class in class_list:
        if exists(join(target_dir, _class.filename)):
            target_dir_class = _class

    return (target_dir, target_dir_class, subdirs)
