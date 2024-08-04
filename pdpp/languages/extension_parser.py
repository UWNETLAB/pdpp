from typing import List

from pdpp.languages.language_enum import Language
from pdpp.tasks.base_task import BaseTask


def extension_parser(task: BaseTask) -> List[str]:
    extension_list = []

    for entry in task.src_files:
        extension_list.append(str(entry).split(".")[-1].lower())

    language_list = []

    for entry in extension_list:
        if entry == "py":
            language_list.append(Language.PYTHON.value)
        elif entry == "r" or entry == "rscript":
            language_list.append(Language.R.value)
        else:
            language_list.append("???")

    return language_list
