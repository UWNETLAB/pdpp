from click import clear as click_clear

from pdpp.languages.extension_parser import extension_parser
from pdpp.languages.language_enum import Language
from pdpp.tasks.base_task import BaseTask
from pdpp.utils.prompt_helpers import prompt_or_abort


def q4(task: BaseTask) -> str:
    """
    This question is used to determine the language of the source code this task will run.
    """

    click_clear()

    language_list = extension_parser(task)

    if len(set(language_list)) != 1 or "???" in language_list:
        message = """Note that pdpp does not currently support automating tasks that
        contain scripts written in more than one programming language.

        If this task contains source code from multiple languages,
        please separate all source code written in dissimilar
        languages into different tasks. Failing to do so will
        cause an exception at runtime.

        If all of this task's source code is written in the same
        pdpp-supported language, you can indicate the appropriate
        language below.

        If the programming language you would like to use is not
        indicated below, or you would like to use more than one programming
        language in the same task, consider creating a custom pdpp task using
        the 'pdpp custom' command.

        Select the programming language used:
        """

        question_4 = [
            {
                "type": "list",
                "name": "language",
                "message": message,
                "choices": [
                    {"name": Language.PYTHON.value},
                    {"name": Language.R.value},
                ],
            }
        ]

        return prompt_or_abort(question_4, "language")

    else:
        return language_list[0]
