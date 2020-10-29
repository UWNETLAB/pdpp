"""The primary access point for the `pdpp` package.

Every call to `pdpp` from the command line is routed through this
module.
"""

from pdpp.utils.step_folder_test import StepFolder
from pdpp.utils.directory_test import in_project_folder
from pdpp.utils.rem_slash import rem_slash
from pdpp.styles.graph_style import default_graph_style, greyscale_graph_style, base_graph_style
import os
import click
from typing import List, Type


GRAPH_STYLE_LIST: List[Type[base_graph_style]] = [default_graph_style, greyscale_graph_style] 
CONTEXT_SETTINGS = dict(help_option_names=['-h', '--help'])
FILES_LIST = ['png', 'pdf', 'both']


@click.group()
def main():
    """A command line tool to automate the use of the Principled Data Processing methodology for reproducibility."""
    
    pass


# init
@main.command(short_help="Prepares a directory to become a pdpp project")
def init():

    from pdpp.templates.populate_new_project import populate_new_project
    populate_new_project()


# new
@main.command(short_help="Creates a new directory named <dirname>, with subdirectories 'input', "
                         "'output', and 'src'. Adds dodo.py to <dirname>. Use this to create a new step folder. "
                         "You will be asked to indicate which other steps are dependencies of this step,"
                         "And which files from those steps should be immediately linked to the new step.",
              context_settings=CONTEXT_SETTINGS)
@click.option('--dirname', '-d',
              type=StepFolder(),
              prompt="What do you want to call the new task directory?"
                     "(Use all lower case, no spaces, and cannot be '_import_' or '_export_')",
              help="This is what you want to name your new step folder. "
                   "It must be all lower case and contain no spaces."
              )
def new(dirname):
    """Creates a new directory named <dirname>, with subdirectories 'input', 'output', and 'src'.
    Adds dodo.py to <dirname>. Use this to create a new step folder."""
    
    in_project_folder()

    from pdpp.task_types.step_task import StepTask

    StepTask(target_dir = rem_slash(dirname)).initialize_task()
    
    click.echo(f"Your new step folder, {dirname}, was created.")


# rig
@main.command(short_help="Incorporates a step in the project's automation")
def rig():
    in_project_folder()
    from pdpp.questions.question_0 import q0
    q0().rig_task()


#TODO: custom
@main.command(short_help="Creates a new directory named <dirname>, with subdirectories 'input', "
                         "'output', and 'src'. Adds dodo.py to <dirname>. Use this to create a new step folder. "
                         "You will be asked to indicate which other steps are dependencies of this step,"
                         "And which files from those steps should be immediately linked to the new step.",)
@click.option('--dirname', '-s',
              type=StepFolder(),
              prompt="What do you want to call the new custom task directory?"
                     "(Use all lower case, no spaces, and cannot be '_import_' or '_export_')",
              help="This is what you want to name your new step folder. "
                   "It must be all lower case and contain no spaces."
              )
def custom(dirname: str):
    """Creates a new directory named <dirname>, with subdirectories 'input', 'output', and 'src'.
    Adds dodo.py to <dirname>. Use this to create a new step folder."""

    in_project_folder()

    from pdpp.task_types.custom_task import CustomTask

    CustomTask(target_dir = rem_slash(dirname)).initialize_task()
    
    click.echo(f"Your new step folder, {dirname}, was created.")


#TODO sub
@main.command(short_help="Creates a new subproject in a directory named <dirname>,"
                         "You will be asked to indicate which other steps are dependencies of this step,"
                         "And which files from those steps should be immediately linked to the new step.",)
@click.option('--dirname', '-s',
              type=StepFolder(),
              prompt="What do you want to call the new subproject task directory?"
                     "(Use all lower case, no spaces, and cannot be '_import_' or '_export_')",
              help="This is what you want to name your new step folder. "
                   "It must be all lower case and contain no spaces."
              )
def sub(dirname):
    """Creates a new subproject in a directory named <dirname>.
    Adds dodo.py to <dirname>. Use this to create a new step folder."""

    in_project_folder()

    from pdpp.task_types.sub_task import SubTask

    SubTask(target_dir = rem_slash(dirname)).initialize_task()
    
    click.echo(f"Your new subproject, {dirname}, was created.")

 
#TODO graph
@main.command(short_help="Creates a dependency graph to visualize how the steps in your project relate "
                         "to each other.", context_settings=CONTEXT_SETTINGS)
@click.option('--files', '-f',
              type=click.Choice(FILES_LIST),
              prompt="What file format would you prefer as an output?",
              help="The dependency graph can be outputted in .png and/or .pdf formats. Default is to output both formats.",
              default="both")
@click.option(
    '--style', '-s',
    type=click.Choice([s.NAME for s in GRAPH_STYLE_LIST]),
    prompt="What color scheme would you prefer?",
    help="The dependency graph can be outputted in one of a variety of styles.",
    default=default_graph_style.NAME,
    )
def graph(files, style):
    in_project_folder()
    from pdpp.graph_dependencies import depgraph
    """Creates a dependency graph to visualize how the steps in your project relate to each other."""
    full_style = next((s for s in GRAPH_STYLE_LIST if s.NAME == style), None)
    depgraph(files, full_style)


# run
@main.command(short_help="Runs the project")
def run():
    in_project_folder()
    from pdpp.doit_constructors.doit_run import doit_run
    doit_run()


# enable
@main.command(short_help="Selects which tasks will resolve when pdpp run is called")
def enable():
    in_project_folder()
    from pdpp.task_enabler import task_enabler
    task_enabler()
