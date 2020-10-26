import yaml
from posixpath import join



def dump_self(task):
    with open(type(task).FILENAME, 'w') as stream:
        yaml.dump(task, stream, default_flow_style=False)


def load_task(task_path):
    with open(task_path, 'r') as stream:
        return yaml.full_load(stream)