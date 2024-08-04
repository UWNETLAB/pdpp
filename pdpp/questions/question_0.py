from click import clear as click_clear
from questionary import Choice, prompt

from pdpp.styles.prompt_style import custom_style_fancy
from pdpp.tasks.base_task import BaseTask
from pdpp.utils.directory_test import get_riggable_tasks


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

    return prompt(questions_0, style=custom_style_fancy)["target_dir"]
