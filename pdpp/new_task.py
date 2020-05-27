import os
from pdpp.questions.question_1 import q1
from pdpp.questions.question_2 import q2
from pdpp.questions.question_3 import q3
from pdpp.questions.question_4 import q4
from pdpp.utils.directory_test import get_riggable_directories, get_riggable_classes
import yaml
from pdpp.utils.immediate_link import immediate_link, immediate_import_link
from pdpp.pdpp_class import base_pdpp_class

def create_task(this_class: base_pdpp_class):

    this_class.initialize_step()

    subdirs = get_riggable_directories()
    riggables = get_riggable_classes()

    subdirs.append("_import_")

    subdirs.sort()

    # Question 1 - Which other Steps contain necessary dependencies?
    dep_dirs = q1(subdirs, this_class.target_dir, this_class)

    # Question 2 - Which files from the indicated dependencies are needed?
    if dep_dirs != None:
        if len(dep_dirs) != 0: 
            this_class.dep_files, this_class.import_files = q2(dep_dirs, this_class.target_dir, this_class)
        else:
            this_class.dep_files = []
    else:
        this_class.dep_files = []

    
    immediate_link(this_class, riggables)
    immediate_import_link(this_class)
    
    if this_class.has_source:
        this_class.src_files = q3(this_class.target_dir, this_class)
        this_class.language = q4(this_class.src_files)

    yaml_loc = os.path.join(this_class.target_dir, this_class.filename)

    with open(yaml_loc, 'w') as stream:
        yaml.dump(this_class, stream, default_flow_style=False)
