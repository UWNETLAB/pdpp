"""The primary access point for the `pdpp` package.

Every call to `pdpp` from the command line is routed through this
module.
"""

from pdpp.utils import step_folder 
from pdpp.utils import directory_test
from pdpp.utils.rem_slash import rem_slash
#from pdpp.new_task import create_task
import click
 
CONTEXT_SETTINGS = dict(help_option_names=['-h', '--help'])
files_list = ['png', 'pdf', 'both']


@click.group()
def main():
    """A command line tool to automate the use of the Principled Data Processing methodology for reproducibility."""
    pass


# init
@main.command(short_help="Prepares a directory to become a pdpp project")
def init():
    from pdpp.templates.project_structure import populate_new_project
    populate_new_project(".")



# new
@main.command(short_help="Creates a new directory named <dirname>, with subdirectories 'input', "
                         "'output', and 'src'. Adds dodo.py to <dirname>. Use this to create a new step folder. "
                         "You will be asked to indicate which other steps are dependencies of this step,"
                         "And which files from those steps should be immediately linked to the new step.",
              context_settings=CONTEXT_SETTINGS)
@click.option('--dirname', '-d',
              type=step_folder.StepFolder(),
              prompt="What do you want to call the new task directory?"
                     "(Use all lower case, no spaces, and cannot be '_import_' or '_export_')",
              help="This is what you want to name your new step folder. "
                   "It must be all lower case and contain no spaces."
              )
def new(dirname):
    """Creates a new directory named <dirname>, with subdirectories 'input', 'output', and 'src'.
    Adds dodo.py to <dirname>. Use this to create a new step folder."""
    directory_test.in_project_folder()

    from pdpp.task_types.step_task import StepTask

    class_type = StepTask(target_dir = rem_slash(dirname))
    
    create_task(class_type)
    click.echo(f"Your new step folder, {dirname}, was created.")


#custom
@main.command(short_help="Creates a new directory named <dirname>, with subdirectories 'input', "
                         "'output', and 'src'. Adds dodo.py to <dirname>. Use this to create a new step folder. "
                         "You will be asked to indicate which other steps are dependencies of this step,"
                         "And which files from those steps should be immediately linked to the new step.",)
@click.option('--dirname', '-s',
              type=step_folder.StepFolder(),
              prompt="What do you want to call the new custom task directory?"
                     "(Use all lower case, no spaces, and cannot be '_import_' or '_export_')",
              help="This is what you want to name your new step folder. "
                   "It must be all lower case and contain no spaces."
              )
def custom(dirname):
    """Creates a new directory named <dirname>, with subdirectories 'input', 'output', and 'src'.
    Adds dodo.py to <dirname>. Use this to create a new step folder."""
    directory_test.in_project_folder()

    from pdpp.pdpp_class import custom_class

    class_type = custom_class(target_dir = rem_slash(dirname))
    
    create_task(class_type)
    click.echo(f"Your new step folder, {dirname}, was created.")


#sub
@main.command(short_help="Creates a new subproject in a directory named <dirname>,"
                         "You will be asked to indicate which other steps are dependencies of this step,"
                         "And which files from those steps should be immediately linked to the new step.",)
@click.option('--dirname', '-s',
              type=step_folder.StepFolder(),
              prompt="What do you want to call the new subproject task directory?"
                     "(Use all lower case, no spaces, and cannot be '_import_' or '_export_')",
              help="This is what you want to name your new step folder. "
                   "It must be all lower case and contain no spaces."
              )
def sub(dirname):
    """Creates a new subproject in a directory named <dirname>.
    Adds dodo.py to <dirname>. Use this to create a new step folder."""
    directory_test.in_project_folder()

    from pdpp.pdpp_class import project_class

    class_type = project_class(target_dir = rem_slash(dirname))
    
    create_task(class_type)
    click.echo(f"Your new subproject, {dirname}, was created.")


# rig
@main.command(short_help="Incorporates a step in the project's automation")
def rig():
    directory_test.in_project_folder()
    from pdpp.rig import rig as rig_step
    rig_step()

 
# graph
@main.command(short_help="Creates a dependency graph to visualize how the steps in your project relate "
                         "to each other.", context_settings=CONTEXT_SETTINGS)
@click.option('--files', '-f',
              type=click.Choice(files_list),
              prompt="What file format would you prefer as an output?",
              help="The dependency graph can be outputted in .png and/or .pdf formats. Default is to output both formats.",
              default="both")
def graph(files):
    directory_test.in_project_folder()
    from pdpp.graph_dependencies import depgraph
    """Creates a dependency graph to visualize how the steps in your project relate to each other."""
    depgraph(files)


# run
@main.command(short_help="Runs the project")
def run():
    directory_test.in_project_folder()
    from pdpp.doit_constructors.doit_run import doit_run
    doit_run()


# select
@main.command(short_help="Selects which tasks will resolve when pdpp run is called")
def select():
    directory_test.in_project_folder()
    from pdpp.task_enabler import task_enabler
    task_enabler()


