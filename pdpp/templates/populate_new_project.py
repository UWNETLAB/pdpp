from pdpp.templates.create_gitignore import create_gitignore
from pdpp.templates.dodo_template import create_dodo_template
from pdpp.task_types.export_task import ExportTask
from pdpp.task_types.import_task import ImportTask


def populate_new_project():
    """
    This is run whenever `pdpp new` and `pdpp sub` is invoked. 
    It checks to see whether the necessary support structure is in place.
    This is also run in a new pdpp subproject. 
    """

    ExportTask().initialize_task()
    ImportTask().initialize_task()
    create_dodo_template()
    create_gitignore()
