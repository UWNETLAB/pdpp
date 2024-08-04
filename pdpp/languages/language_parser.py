from pdpp.languages.language_enum import Language
from pdpp.languages.runners import python_runner, r_runner
from pdpp.tasks.base_task import BaseTask


def parse_language(task: BaseTask):
    if task.language == Language.PYTHON.value:
        return python_runner
    elif task.language == Language.R.value:
        return r_runner
    else:
        raise Exception
