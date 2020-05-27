from questionary import Separator, prompt
from click import clear as click_clear
from posixpath import join
import os
from pprint import pprint
from pdpp.styles.prompt_style import custom_style_fancy
from pdpp.pdpp_class import step_class
from typing import Tuple, List, Dict
from pdpp.utils.directory_test import get_riggable_classes

def q2(dep_dirs: list, target_dir: str, step_metadata:step_class) -> Tuple[Dict[str, List[str]], List[str]]:
    """
    A question which asks users to indicate which individual files 
    (drawn from a list of those contained in the output directories of the steps indicated in question #1) 
    are required as dependencies for the current step.
    """

    click_clear()

    q2input = {}
    import_input = []

    riggable_classes = get_riggable_classes()
    selected_classes = []

    import_dir = "_import_"

    include_import = False

    if import_dir in dep_dirs:
        dep_dirs.remove(import_dir)
        include_import = True

    for directory in dep_dirs:
        selected_class = next((c for c in riggable_classes if c.target_dir == directory))
        selected_classes.append(selected_class)

    for selected_class in selected_classes:
        q2input[selected_class.target_dir] = []
        for root, _, files in os.walk(join(selected_class.target_dir, selected_class.out_dir)):
            root = root.replace('\\', '/').replace('./', '').replace('.\\', '')
            for entry in files:
                if entry != '.gitkeep' and entry != "pdpp_export.yaml":
                    output = join(root, entry).replace('./', '')
                    q2input[selected_class.target_dir].append(output) 

    if include_import:
        for root, _, files in os.walk(import_dir):
            root = root.replace('\\', '/').replace('./', '').replace('.\\', '')
            for entry in files:
                if entry != '.gitkeep' and entry != "pdpp_export.yaml":
                    output = join(root, entry).replace('./', '')
                    import_input.append(output) 

    choice_list_2 = []

    for key in q2input:
        if len(q2input[key]) > 0:
            choice_list_2.append(Separator('\n= ' + key + ' ='))
            for value in q2input[key]:
                try:
                    checked = join(*(value.split('/')[2:])) in step_metadata.dep_files[key]
                except KeyError:
                    checked = False
                choice_list_2.append({
                    'name': join(value),
                    'checked': checked,
                    })

        else:
            print(str(key) + " does not contain any eligible output files. Skipping.")

    if include_import:
        if len(import_input) > 0:
            choice_list_2.append(Separator('\n= ' + import_dir + ' ='))
            for value in import_input:
                try:
                    checked = join(*(value.split('/')[1:])) in step_metadata.import_files
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

    response_dict={}
    import_list = []

    if len(questions_2[0]['choices']) > 0:
        responses = prompt(questions_2, style=custom_style_fancy)['dependencies']
    else:
        return (response_dict, import_list)

    for response in responses:
        split_response = response.split('/')

        pprint(split_response)

        if split_response[0] == import_dir:
            
            dependency_step_name = split_response.pop(0)

            import_list.append(join(*split_response))

        else:
            #The following line 'pops' the step name out of the list of the components which comprise the
            #dependency filepath... The one thereafter pops out the one following, which will always be 'output'
            dependency_step_name = split_response.pop(0)

            _ = split_response.pop(0)

            if dependency_step_name in response_dict:
                pass
            else:
                response_dict[dependency_step_name] = []
            
            response_dict[dependency_step_name].append(join(*split_response))

    return (response_dict, import_list)