from typing import List

from click import clear as click_clear
from questionary import Choice, prompt

from pdpp.styles.prompt_style import custom_style_fancy
from pdpp.tasks.base_task import BaseTask


def q1(dep_tasks: List[BaseTask], task: BaseTask) -> List[BaseTask]:
    """
    This question is used to determine which other tasks in the project structure
    are dependencies of the current task.
    """

    click_clear()

    choice_list = []

    """
    First, add all the project subdirectories (riggable_subdirectories) returned
    from Question 0. When this process encounters the task being rigged (target_dir),
    add it to the list as a disabled entry.
    """

    for dep_task in dep_tasks:
        if dep_task.target_dir == task.target_dir:
            choice_list.append(
                Choice(
                    title=dep_task.target_dir,
                    value=dep_task,
                    disabled="This is the selected task",
                )
            )

        else:
            choice_list.append(
                Choice(
                    title=dep_task.target_dir,
                    value=dep_task,
                    checked=dep_task.target_dir in task.dep_files,
                )
            )

    if len(choice_list) < 1:
        return []

    # sort the choice_list alphabetically
    choice_list.sort(key=lambda choice: choice.title)

    questions_1 = [
        {
            "type": "checkbox",
            "message": 'Select tasks which contain dependencies for "{}"'.format(
                task.target_dir
            ),
            "name": "dep_tasks",
            "choices": choice_list,
        }
    ]

    return prompt(questions_1, style=custom_style_fancy)["dep_tasks"]
