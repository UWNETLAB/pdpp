from questionary import prompt
from click import clear as click_clear
from os import walk
from posixpath import join
from pdpp.styles.prompt_style import custom_style_fancy
from pdpp.pdpp_class import step_class


def q3(target_dir: str, step_metadata: step_class) -> list:
    """
    A question which asks users to indicate which scripts in the chosen step's 'src' folder
    should be run in order to produce this step's targets.
    """

    click_clear()

    source_files = []
    source_choices = []

    for _, _, files in walk(join(target_dir, 'src')):
        for script in files: 
            if script != '.gitkeep':
                source_choices.append({
                    'name': script,
                    'checked': script in step_metadata.src_files,
                })  
                source_files.append(script)

    if len(source_files) < 2:
        return source_files

    question_3 = [{
            'type': 'checkbox',
            'message': 'Select the source files for "{}"'.format(target_dir),
            'name': 'source',
            'choices': source_choices,
        }]

    return prompt(question_3, style=custom_style_fancy)['source']