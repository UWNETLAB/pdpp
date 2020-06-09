from posixpath import join
from pdpp.doit_constructors.link_task import make_link_task
from pdpp.utils.directory_test import get_riggable_classes
from typing import List, Tuple
from pdpp.pdpp_class import base_pdpp_class, export_class, custom_class, project_class, step_class, import_class
from pdpp.languages.language_parser import parse_language
from pdpp.languages.runners import project_runner


#####
#
# Of all of the scripts contained in pdpp, this one is the most in need
# of major overhauls. I'm going to use a system of 'question and answer'
# comments as notes to myself to try and sort out what needs to be done
#
#####

def passaction():
    pass

def class_list_splitter(loaded_steps: List[base_pdpp_class]) -> Tuple[export_class, List[custom_class], List[project_class], List[step_class]]:

    _export: export_class = [] 
    custom_list: List[custom_class] = []
    project_list: List[project_class] = []
    step_list: List[step_class] = []

    for entry in loaded_steps:
        if isinstance(entry, export_class):
            _export = entry
        elif isinstance(entry, custom_class):
            custom_list.append(entry)
        elif isinstance(entry, project_class):
            project_list.append(entry)
        elif isinstance(entry, step_class):
            step_list.append(entry)
        else:
            print("something went wrong")
            raise Exception
    
    return (_export, custom_list, project_list, step_list)

def find_dependencies_from_others(step: base_pdpp_class, export:export_class, list_of_lists: List[List[base_pdpp_class]]) -> List:

    deps_from_others = set()

    for class_list in list_of_lists:
        for other_step in class_list:
            if step.target_dir in other_step.dep_files:
                for entry in other_step.dep_files[step.target_dir]:
                    deps_from_others.add(entry)

    if step.target_dir in export.dep_files:
        for entry in export.dep_files[step.target_dir]:
            deps_from_others.add(entry)

    return list(deps_from_others)
 
def gen_many_tasks():
    
    # 1. Get all of the steps in the current scope
    loaded_steps = get_riggable_classes()


    # 2. Create a list of all the disabled steps loaded in step #1
    disabled_list = []

    for step in loaded_steps:
        if step.enabled == False:
            disabled_list.append(step)


    #####
    #
    # Here's where the real mess begins. This portion of the code is iterating through
    # all of the loaded steps and doing the following, in order, for each:
    # 
    # 1. 
    #
    #####

    _export, custom_list, project_list, step_list = class_list_splitter(loaded_steps)

    step_and_custom: List[base_pdpp_class] = step_list + custom_list + project_list + [_export]
    
    for step in step_and_custom:
        print(step.__class__)

        if step.enabled == False:
            pass

        else:
            dep_list = []

            """
            The following, which is a new addition to pdpp, examines the dependencies of all other 
            steps in order to determine what targets the current step should have. 
            """

            targ_list = find_dependencies_from_others(step, _export, [custom_list, project_list, step_list])

            yield make_link_task(step, loaded_steps, disabled_list)
            
            action_list = []

            if isinstance(step, project_class):
                action_list.append((project_runner, [step.target_dir], {}))
            elif isinstance(step, custom_class):
                action_list = step.shell_commands
            elif isinstance(step, step_class):
                runner = parse_language(step)
                for source_file in step.src_files:
                    action_list.append((runner, [source_file, step.target_dir], {}))
                    dep_list.append(join(step.target_dir, step.src_dir, source_file))
            elif isinstance(step, export_class):
                action_list.append((passaction, [], {}))
            else:
                raise Exception


            """
            This section adds all of the file dependencies to the metadata being passed to doit. This information is drawn from the
            "dep_files" dictionary that all step .yaml files have, as well as their "import_files" attribute.
            """

            for dependent_step in step.dep_files:
                for dependency_file in step.dep_files[dependent_step]:
                    dep_list.append(join(step.target_dir, step.in_dir, dependency_file))

            
            full_targ_list = [join(step.target_dir, step.out_dir, targ) for targ in targ_list]

            print(step.target_dir)
            print(dep_list)
            print("")


            yield {
                'basename': '{}'.format(step.target_dir),
                'actions': action_list,
                'file_dep': dep_list,
                'targets': full_targ_list,
                'clean': True,
            }


def task_all():
    yield gen_many_tasks()

if __name__ == '__main__':
    import doit
    doit.run(globals())