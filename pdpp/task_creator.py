from posixpath import join
from pdpp.utils.directory_test import get_pdpp_tasks
from typing import List
from pdpp.pdpp_class_base import BasePDPPClass
from pdpp.languages.language_parser import parse_language
from pdpp.languages.runners import project_runner
from pdpp.doit_constructors.link_task import make_link_task


def find_dependencies_from_others(task: BasePDPPClass, loaded_steps: List[BasePDPPClass]) -> List[str]:

    dependencies = []

    for other_task in loaded_steps:
        dependencies.extend(other_task.provide_dependencies(task))

    return [d for d in set(dependencies)] # This is just a hackier way of making everything unique; pylance type checking REALLY didn't like list(set(dependencies)) for some reason
 
def gen_many_tasks():
    
    # 1. Get all of the steps in the current scope
    loaded_tasks = get_pdpp_tasks()

    # 2. Create a list of all the disabled steps loaded in step #1
    disabled_list = [t.target_dir for t in loaded_tasks if not t.enabled]

    for task in loaded_tasks:

        target_list = find_dependencies_from_others(task, loaded_tasks)

        yield make_link_task(task, disabled_list)

        if task.enabled and task.RUN_VALID:
            pass
            
            

            
            
            # yield {
            #     'basename': f'{task.target_dir}',
            #     'actions': action_list,
            #     'file_dep': dep_list,
            #     'targets': target_list,
            #     'clean': True,
            # }


def task_all():
    yield gen_many_tasks()

if __name__ == '__main__':
    import doit
    doit.run(globals())



    #         action_list = []

    #         if isinstance(step, project_class):
    #             action_list.append((project_runner, [step.target_dir], {}))
    #         elif isinstance(step, custom_class):
    #             action_list = step.shell_commands
    #         elif isinstance(step, step_class):
    #             runner = parse_language(step)
    #             for source_file in step.src_files:
    #                 action_list.append((runner, [source_file, step.target_dir], {}))
    #                 dep_list.append(join(step.target_dir, step.src_dir, source_file))
    #         elif isinstance(step, export_class):
    #             action_list.append((passaction, [], {}))
    #         else:
    #             raise Exception


    #         """
    #         This section adds all of the file dependencies to the metadata being passed to doit. This information is drawn from the
    #         "dep_files" dictionary that all step .yaml files have, as well as their "import_files" attribute.
    #         """

    #         for dependent_step in step.dep_files:
    #             for dependency_file in step.dep_files[dependent_step]:
    #                 dep_list.append(join(step.target_dir, step.in_dir, dependency_file))