from pdpp.pdpp_class import base_pdpp_class
from pdpp.languages.runners import python_runner, r_runner

def parse_language(step: base_pdpp_class):

    if step.language == "Python":
        return python_runner
    elif step.language == "R":
        return r_runner
    else:
        raise Exception



