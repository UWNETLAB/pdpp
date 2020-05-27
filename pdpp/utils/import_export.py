from os import listdir, remove
from posixpath import join, isdir, exists
from shutil import rmtree
from pdpp.utils.immediate_link import immediate_link
import yaml
from pdpp.pdpp_class import export_class, base_pdpp_class
from typing import List

def create_export(export_class_instance: export_class, riggable_classes: List[base_pdpp_class]):
    """
    This is a docstring.
    """

    filepaths = listdir("_export_")

    for filepath in filepaths:
        if filepath != ".gitkeep":
            full_filepath = join("_export_", filepath)

            if isdir(full_filepath):
                rmtree(full_filepath)
            elif exists(full_filepath):
                remove(full_filepath)
                

    immediate_link(export_class_instance, riggable_classes)

    with open("_export_/pdpp_export.yaml", 'w') as stream:
        yaml.dump(export_class_instance, stream, default_flow_style = False)
