import os
from os import DirEntry
from posixpath import join
from typing import Dict, List, Tuple

from click import clear as click_clear
from questionary import Choice, Separator, prompt

from pdpp.styles.prompt_style import custom_style_fancy
from pdpp.tasks.base_task import BaseTask
from pdpp.templates.dep_dataclass import dep_dataclass
from pdpp.utils.ignorelist import ignorelist


def q2(selected_dep_tasks: List[BaseTask], task: BaseTask) -> Dict[str, dep_dataclass]:
    """
    A question which asks users to indicate which individual files
    (drawn from a list of those contained in the output directories of the tasks
    indicated in question #1) are required as dependencies for the current task.
    """

    click_clear()

    q2input: Dict[BaseTask, List[DirEntry[str]]] = {}

    for selected_task in selected_dep_tasks:
        search_dir = join(selected_task.target_dir, selected_task.OUT_DIR)

        results = [r for r in os.scandir(search_dir) if r.name not in ignorelist]

        if results:
            q2input[selected_task] = results

    choice_list = []

    for key, values in q2input.items():
        choice_list.append(Separator("\n= " + key.target_dir + " ="))

        for value in values:
            try:
                checked = (
                    value.name in task.dep_files[key.target_dir].dir_list
                    or value.name in task.dep_files[key.target_dir].file_list
                )
            except KeyError:
                checked = False
            except TypeError:
                checked = False

            title = value.name

            if value.is_dir():
                title += " (This is a directory)"

            choice_list.append(
                Choice(
                    title=title,
                    value=(key, value),
                    checked=checked,
                )
            )

    # sort the choice_list alphabetically
    choice_list.sort(key=lambda choice: choice.title)
    
    questions_2 = [
        {
            "type": "checkbox",
            "message": 'Select the dependency files for "{}"'.format(task.target_dir),
            "name": "dependencies",
            "choices": choice_list,
        }
    ]

    response_dict = {}

    responses: List[Tuple[BaseTask, DirEntry[str]]]

    if questions_2[0]["choices"]:
        responses = prompt(questions_2, style=custom_style_fancy)["dependencies"]
    else:
        return {}

    dep_task_set = set([t for t, f in responses])

    for dep_task in dep_task_set:
        file_list = [f.name for t, f in responses if t == dep_task and f.is_file()]
        dir_list = [d.name for t, d in responses if t == dep_task and d.is_dir()]

        response_dict[dep_task.target_dir] = dep_dataclass(
            task_out=dep_task.OUT_DIR,
            task_name=dep_task.target_dir,
            file_list=file_list,
            dir_list=dir_list,
        )

    return response_dict
