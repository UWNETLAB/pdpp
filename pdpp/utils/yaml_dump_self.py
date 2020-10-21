import yaml
from posixpath import join
from pdpp.pdpp_class_base import BasePDPPClass


def yaml_dump_self(self: BasePDPPClass):
    target = join(self.target_dir, type(self).FILENAME)
    with open(target, 'w') as stream:
        yaml.dump(self, stream, default_flow_style=False)
