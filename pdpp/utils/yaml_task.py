import yaml


def dump_self(task):
    with open(type(task).FILENAME, "w") as stream:
        yaml.dump(task, stream, default_flow_style=False)


def load_task(task_path):
    from pdpp.tasks.custom_task import CustomTask
    from pdpp.tasks.export_task import ExportTask
    from pdpp.tasks.import_task import ImportTask
    from pdpp.tasks.standard_task import StandardTask
    from pdpp.tasks.sub_task import SubTask

    with open(task_path, "r") as stream:
        return yaml.load(stream, Loader=yaml.Loader)
