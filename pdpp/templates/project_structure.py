from pdpp.templates.create_gitignore import create_gitignore
from pdpp.templates.dodo_template import create_dodo_template
from pdpp.pdpp_class_base import BasePDPPClass
from pdpp.task_types.export_task import ExportTask
from pdpp.task_types.import_task import ImportTask

from os import makedirs, chdir
from posixpath import join, exists
import yaml 


def create_in_out_src(target_dir):

    """
    Creates the input, output, and src directories, as well as a source file and .gitkeep files, in the new step.
    Only applicable to pdpp_step (pdpp new) and pdpp_custom (pdpp custom) steps.

    """

    makedirs(join(target_dir, "input"))
    makedirs(join(target_dir, "output"))
    makedirs(join(target_dir, "src"))
    

    f = open(join(target_dir, "input", ".gitkeep"), "a")
    f.close()

    f = open(join(target_dir, "output", ".gitkeep"), "a")
    f.close()

    f = open(join(target_dir, "src", ".gitkeep"), "a")
    f.close()

    f = open(join(target_dir, "src", (target_dir + ".py")), "a")
    f.close()


def populate_new_project(target_dir = "."):
    """
    This is run whenever `pdpp new` and `pdpp sub` is invoked. 
    It checks to see whether the necessary support structure is in place.
    This is also run in a new pdpp subproject. 
    """
    chdir(target_dir)
    
    ExportTask().initialize_step()
    ImportTask().initialize_step()
    create_dodo_template()
    create_gitignore()