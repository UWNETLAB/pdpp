from pdpp.tasks.export_task import ExportTask
from pdpp.tasks.import_task import ImportTask
from pdpp.templates.create_gitignore import create_gitignore
from pdpp.templates.dodo_template import create_dodo_template


def populate_new_project(_=None):
    """
    This is run whenever `pdpp new` and `pdpp sub` is invoked.
    It checks to see whether the necessary support structure is in place.
    This is also run in a new pdpp subproject.
    """

    ExportTask().initialize_task()
    ImportTask().initialize_task()
    create_dodo_template()
    create_gitignore()
