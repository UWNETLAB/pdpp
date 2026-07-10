import click
from questionary import Choice

from pdpp.utils.directory_test import get_runnable_tasks
from pdpp.utils.prompt_helpers import prompt_or_abort


def task_enabler():
    runnable_tasks = get_runnable_tasks()

    if not runnable_tasks:
        click.echo("There are no valid tasks in this project directory!")
        return

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

    enabled_list = prompt_or_abort(questions_1, "enabled")

    for task in runnable_tasks:
        if task in enabled_list:
            task.enable()
        elif task not in enabled_list:
            task.disable()
        else:
            raise Exception("SOMETHING WENT WRONG WITH ENABLE FLOW CONTROL")
