from os import DirEntry, scandir
from posixpath import join
from typing import List

from click import clear as click_clear
from questionary import Choice, prompt

from pdpp.styles.prompt_style import custom_style_fancy
from pdpp.tasks.base_task import BaseTask
from pdpp.utils.ignorelist import ignorelist


def q3(task: BaseTask) -> List[str]:
    """
    A question which asks users to indicate which scripts in the chosen task's
    'src'  should be run to produce this task's targets.
    """

    click_clear()

    source_files = []
    source_choices = []
    src_loc = join(task.target_dir, task.SRC_DIR)

    source_files = [
        s for s in scandir(src_loc) if ((s.name not in ignorelist) and (s.is_file()))
    ]

    for entry in source_files:
        source_choices.append(
            Choice(title=entry.name, value=entry, checked=entry.name in task.src_files)
        )

    if len(source_files) < 2:
        return [s.name for s in source_files]

    # sort the choice_list alphabetically
    choice_list.sort(key=lambda choice: choice.title)
    
    question_3 = [
        {
            "type": "checkbox",
            "message": 'Select the source file(s) for "{}"'.format(task.target_dir),
            "name": "source",
            "choices": source_choices,
        }
    ]

    final_choices: List[DirEntry[str]] = prompt(question_3, style=custom_style_fancy)[
        "source"
    ]

    return [s.name for s in final_choices]
