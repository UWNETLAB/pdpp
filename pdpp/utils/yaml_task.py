import yaml
from posixpath import join
from pdpp.pdpp_class_base import BasePDPPClass


def dump_self(task: BasePDPPClass):
    with open(type(task).FILENAME, 'w') as stream:
        yaml.dump(task, stream, default_flow_style=False)


def load_task(task_path):
    with open(task_path, 'r') as stream:
        return yaml.full_load(stream)