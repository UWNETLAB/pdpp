from click import clear as click_clear
from questionary import Choice

from pdpp.tasks.base_task import BaseTask
from pdpp.utils.directory_test import get_riggable_tasks
from pdpp.utils.prompt_helpers import prompt_or_abort


def q0() -> BaseTask:
    """
    This question is used to select the task you wish to alter with pdpp.
    """

    tasks = get_riggable_tasks()

    click_clear()

    choice_list = []

    for task in tasks:
        choice_list.append(
            Choice(
                title=task.target_dir,
                value=task,
            )
        )

    # sort the choice_list alphabetically
    choice_list.sort(key=lambda choice: choice.title)

    questions_0 = [
        {
            "type": "list",
            "name": "target_dir",
            "message": "Select the task you would like to rig:",
            "choices": choice_list,
        }
    ]

    return prompt_or_abort(questions_0, "target_dir")

