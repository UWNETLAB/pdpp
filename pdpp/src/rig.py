def rig():
    import os
    from os.path import isdir, exists
    from posixpath import join
    from pdpp.src.questions.question_0 import q0 as q0
    from pdpp.src.questions.question_1 import q1 as q1
    from pdpp.src.questions.question_2 import q2 as q2
    from pdpp.src.questions.question_2_A import q2_A as q2_A
    from pdpp.src.questions.question_3 import q3 as q3
    from pdpp.src.questions.question_4 import q4 as q4
    from pdpp.src.questions.question_5 import q5 as q5
    from pdpp.src.questions.question_6 import q6 as q6
    from pdpp.src.utils.immediate_link import immediate_link
    from pprint import pprint
    import yaml
    from pdpp.src.styles.prompt_style import custom_style_fancy 
    from pdpp.src.yaml_handlers.import_yaml import import_yaml
    from pdpp.src.utils.proj_folder_test import proj_folder_test


    # Question 0 - Which Step are you Rigging?
    target_dir, subdirs = q0(proj_folder_test, custom_style_fancy)
    yaml_dict, yaml_loc = import_yaml(target_dir)

    # Question 1 - Which other Steps contain necessary dependencies?
    dep_dirs = q1(subdirs, target_dir, yaml_dict['dep_dirs'], custom_style_fancy)

    # Question 2 - Which files from the indicated dependencies are needed?
    if len(dep_dirs) != 0 and dep_dirs != None:
        dep_files, dep_dirs = q2(dep_dirs, target_dir, yaml_dict['dep_files'], custom_style_fancy)
    else:
        dep_files = {}
        dep_dirs = []
    
    immediate_link(dep_files)

    # Question 2_A - If any of this step's dependencies DO NOT originate from another step in the workflow, indicate them here:
    self_deps = q2_A(target_dir, yaml_dict['self_deps'], dep_files, custom_style_fancy)
    
    # Question 3 - Which files in the src foler should be treated as dependencies?
    src_files = q3(target_dir, yaml_dict['src_files'], custom_style_fancy)

    # Question 4 - Which programming language was this step written in?
    language = q4(src_files, custom_style_fancy)

    # Question 5 - Are the targets for this step ready to be Rigged?
    target_status = q5(target_dir, custom_style_fancy)

    # Question 6 - 
    if target_status:
        target_files = q6(target_dir, yaml_dict['target_files'], custom_style_fancy)
    else:
        target_files = []

    step_dict = {
        'target_dir': target_dir,
        'dep_dirs': dep_dirs,
        'dep_files': dep_files,
        'src_files': src_files,
        'language': language,
        'target_status': target_status,
        'target_files': target_files,
        'self_deps': self_deps,
        'enabled': yaml_dict['enabled'],
        }

    pprint(step_dict)

    with open(yaml_loc, 'w') as stream:
        yaml.dump(step_dict, stream, default_flow_style=False)

if __name__ == '__main__':
    rig()
