import os
from pdpp.questions.question_1 import q1
from pdpp.questions.question_2 import q2
from pdpp.questions.question_3 import q3
from pdpp.questions.question_4 import q4
from pdpp.utils.directory_test import get_riggable_classes
import yaml
from pdpp.utils.immediate_link import immediate_link, immediate_import_link
from pdpp.pdpp_class_base import BasePDPPClass

def create_task(task: BasePDPPClass):

    task.initialize_step()

    riggables, subdirs = get_riggable_classes()

    subdirs.append("_import_")

    subdirs.sort()

    # Question 1 - Which other Steps contain necessary dependencies?
    dep_dirs = q1(subdirs, task.target_dir, task)

    # Question 2 - Which files from the indicated dependencies are needed?
    if dep_dirs != None:
        if len(dep_dirs) != 0: 
            task.dep_files, task.import_files = q2(dep_dirs, task.target_dir, task)
        else:
            task.dep_files = {}
    else:
        task.dep_files = {}

    
    immediate_link(task, riggables)
    immediate_import_link(task)
    
    if task.has_source:
        task.src_files = q3(task.target_dir, task)
        task.language = q4(task.src_files)

    yaml_loc = os.path.join(task.target_dir, task.filename)

    with open(yaml_loc, 'w') as stream:
        yaml.dump(task, stream, default_flow_style=False)
