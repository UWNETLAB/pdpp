from pdpp.pdpp_class import base_pdpp_class, import_class
from pdpp.doit_constructors.mylinker import mylinker
from typing import List
from posixpath import join


def make_link_task(step: base_pdpp_class, loaded_steps: List[base_pdpp_class], disabled_list: List[base_pdpp_class]):

    if len(step.import_files) > 0:
        step.dep_files["_import_"] = step.import_files

    import_instance = import_class()

    loaded_steps.append(import_instance)

    for linking_task_name in step.dep_files:

        link_class = next((c for c in loaded_steps if c.target_dir == linking_task_name))

        link_action_list = [] 
        link_dep_list = []
        link_targ_list = []

        if link_class in disabled_list:
            print('DISABLED')
            pass
        
        else:
            for filename in step.dep_files[link_class.target_dir]:

                link_start = join(link_class.target_dir, link_class.out_dir, filename)
                link_end = join(step.target_dir, step.in_dir, filename)

                link_dep_list.append(link_start)
                link_targ_list.append(link_end)
                #dep_list.append(link_end)

                link_action_list.append(
                    (mylinker, [link_start, link_end])
                )

            yield {
                'basename': 'task_{}_LINK_TO_{}'.format(link_class.target_dir, step.target_dir),
                'actions': link_action_list,
                'file_dep': link_dep_list,
                'targets': link_targ_list,
                'clean': True,
            }