from pdpp.questions.question_0 import q0 as q0
from pdpp.questions.question_1 import q1 as q1
from pdpp.questions.question_2 import q2 as q2
from pdpp.questions.question_3 import q3 as q3
from pdpp.questions.question_4 import q4 as q4
from pdpp.utils.immediate_link import immediate_link, immediate_import_link
from pdpp.utils.import_step_class import import_step_class, export_pdpp_class
from pdpp.pdpp_class import step_class, export_class
from pdpp.utils.import_export import create_export
from pdpp.utils.directory_test import get_riggable_classes

 
def rig():

    # Question 0 - Which Step are you Rigging?
    target_dir, target_dir_class, subdirs = q0() 
    step_metadata = import_step_class(target_dir, target_dir_class.filename)

    # Question 1 - Which other Steps contain necessary dependencies?
    dep_dirs = q1(subdirs, target_dir, step_metadata)

    # Question 2 - Which files from the indicated dependencies are needed?
    if len(dep_dirs) != 0:
        dep_files_dict, import_list = q2(dep_dirs, target_dir, step_metadata)
    else:
        dep_files_dict = {}
        import_list = []

    riggable_classes = get_riggable_classes() 

    if target_dir == "_export_":
        export_class_instance = export_class(dep_files=dep_files_dict)
        create_export(export_class_instance, riggable_classes)

    else:

        step_metadata.dep_files = dep_files_dict
        step_metadata.target_dir = target_dir

        # Immediate Link - links the outputs specified in Question 2 to the Step's input
        immediate_link(step_metadata, riggable_classes)
        immediate_import_link(step_metadata)

        # Question 3 - Which files in the src foler should be treated as dependencies?
        src_files = q3(target_dir, step_metadata)

        # Question 4 - Which programming language was this Step written in?
        language = q4(src_files)

        new_step_metadata = step_class(
            target_dir=str(target_dir), 
            dep_files=dep_files_dict,
            import_files=import_list,
            src_files=src_files,
            language=language,
            enabled=step_metadata.enabled
            )

        export_pdpp_class(new_step_metadata)

