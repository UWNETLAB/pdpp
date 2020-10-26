from pdpp.pdpp_class_base import BasePDPPClass
from pdpp.languages.runners import python_runner, r_runner
from pdpp.languages.language_enum import Language

def parse_language(task: BasePDPPClass):

    if task.language == Language.PYTHON.value:
        return python_runner
    elif task.language == Language.R.value:
        return r_runner
    else:
        raise Exception



