from questionary import Choice, prompt

from pdpp.styles.prompt_style import custom_style_fancy
from pdpp.utils.directory_test import get_runnable_tasks


def task_enabler():
    runnable_tasks = get_runnable_tasks()

    choice_list = []

    for task in runnable_tasks:
        choice_list.append(
            Choice(
                title=task.target_dir,
                value=task,
                checked=task.enabled,
            )
        )

    questions_1 = [
        {
            "type": "checkbox",
            "message": "Select the tasks which will be run when 'pdpp run' is called",
            "name": "enabled",
            "choices": choice_list,
        }
    ]

    try:
        enabled_list = prompt(questions_1, style=custom_style_fancy)["enabled"]
    except IndexError:
        print("There are no valid tasks in this project directory!")
        enabled_list = []

    for task in runnable_tasks:
        if task in enabled_list:
            task.enable()
        elif task not in enabled_list:
            task.disable()
        else:
            raise Exception("SOMETHING WENT WRONG WITH ENABLE FLOW CONTROL")
