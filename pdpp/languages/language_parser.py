from pdpp.pdpp_class_base import BasePDPPClass
from pdpp.languages.runners import python_runner, r_runner

def parse_language(task: BasePDPPClass):

    if task.language == "Python":
        return python_runner
    elif task.language == "R":
        return r_runner
    else:
        raise Exception



