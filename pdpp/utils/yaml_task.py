import yaml


def dump_self(task):
    with open(type(task).FILENAME, 'w') as stream:
        yaml.dump(task, stream, default_flow_style=False)


def load_task(task_path):
    from pdpp.task_types.custom_task import CustomTask
    from pdpp.task_types.export_task import ExportTask
    from pdpp.task_types.import_task import ImportTask
    from pdpp.task_types.step_task import StepTask
    from pdpp.task_types.sub_task import SubTask
    with open(task_path, 'r') as stream:
        return yaml.full_load(stream)