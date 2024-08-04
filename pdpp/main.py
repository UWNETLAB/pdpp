from typing import List, Type

import click

from pdpp.styles.graph_style import (
    base_graph_style,
    default_graph_style,
    greyscale_graph_style,
)
from pdpp.utils.directory_test import in_project_directory
from pdpp.utils.rem_slash import rem_slash
from pdpp.utils.task_directory_test import TaskDirectory

GRAPH_STYLE_LIST: List[Type[base_graph_style]] = [
    default_graph_style,
    greyscale_graph_style,
]
CONTEXT_SETTINGS = dict(help_option_names=["-h", "--help"])
FILES_LIST = ["png", "pdf", "jpg"]


@click.group()
def main() -> None:
    """
    A command line tool to automate the use of the Principled Data Processing
    methodology for reproducibility.
    """
    pass


@main.command(short_help="Prepares a directory to become a pdpp project")
def init() -> None:
    from pdpp.templates.populate_new_project import populate_new_project

    populate_new_project()


@main.command(
    short_help="""Create a new task directory
""",
    context_settings=CONTEXT_SETTINGS,
)
@click.option(
    "--dirname",
    "-d",
    type=TaskDirectory(),
    prompt="What do you want to call the new task directory? "
    "(Use all lower case and no spaces. Do not use '_import_' or '_export_')",
    help="This is what you want to name your new task directory. "
    "It must be all lower case and contain no spaces.",
)
def new(dirname):
    """
    Creates a new directory named <dirname>, with subdirectories
    'input', 'output', and 'src'. Adds dodo.py to <dirname>.
    Use this to create a new task directory.
    """
    in_project_directory()
    from pdpp.tasks.standard_task import StandardTask

    StandardTask(target_dir=rem_slash(dirname)).initialize_task()
    click.echo(f"Your new task directory, {dirname}, was created.")


@main.command(
    short_help="""Configure a task's dependencies and source code
"""
)
def rig():
    in_project_directory()
    from pdpp.questions.question_0 import q0

    q0().rig_task()


@main.command(
    short_help="""Create a new task directory with no automation assumptions
""",
)
@click.option(
    "--dirname",
    "-s",
    type=TaskDirectory(),
    prompt="What do you want to call the new custom task directory? "
    "(Use all lower case and no spaces. Do not use '_import_' or '_export_')",
    help="This is what you want to name your new task directory. "
    "It must be all lower case and contain no spaces.",
)
def custom(dirname: str):
    in_project_directory()
    from pdpp.tasks.custom_task import CustomTask

    CustomTask(target_dir=rem_slash(dirname)).initialize_task()
    click.echo(f"Your new task directory, {dirname}, was created.")


@main.command(
    short_help="""Create a new sub-project directory
""",
)
@click.option(
    "--dirname",
    "-s",
    type=TaskDirectory(),
    prompt="What do you want to call the new subproject task directory? "
    "(Use all lower case and no spaces. Do not use '_import_' or '_export_')",
    help="This is what you want to name your new task directory. "
    "It must be all lower case and contain no spaces.",
)
def sub(dirname):
    """Creates a new subproject in a directory named <dirname>.
    Adds dodo.py to <dirname>. Use this to create a new task directory."""
    in_project_directory()
    from pdpp.tasks.sub_task import SubTask

    SubTask(target_dir=rem_slash(dirname)).initialize_task()
    click.echo(f"Your new subproject, {dirname}, was created.")


# graph
@main.command(
    short_help="""Graph this project's dependency structure
""",
    context_settings=CONTEXT_SETTINGS,
)
@click.option(
    "--files",
    "-f",
    type=click.Choice(FILES_LIST),
    prompt="What file format would you prefer as an output?",
    help=(
        "The dependency graph can be outputted in "
        ".png and/or .pdf formats. Default is to output png."
    ),
    default="png",
)
@click.option(
    "--style",
    "-s",
    type=click.Choice([s.NAME for s in GRAPH_STYLE_LIST]),
    prompt="What color scheme would you prefer?",
    help="The dependency graph can be outputted in one of a variety of styles.",
    default=default_graph_style.NAME,
)
def graph(files, style):
    """
    Creates a dependency graph to visualize how the tasks in your project
    relate to each other.
    """
    in_project_directory()
    from pdpp.utils.graph_dependencies import depgraph

    full_style = next((s for s in GRAPH_STYLE_LIST if s.NAME == style), None)
    depgraph(files, full_style)


# run
@main.command(short_help="""Execute the project's tasks""")
def run():
    in_project_directory()
    from pdpp.automation.doit_run import doit_run

    doit_run()


# enable
@main.command(short_help="Selects which tasks will resolve when the project is run")
def enable():
    in_project_directory()
    from pdpp.automation.task_enabler import task_enabler

    task_enabler()


# extant
@main.command(short_help="Add standard automation to an unautomated directory")
def extant():
    in_project_directory()
    from pdpp.questions.question_extant import q_extant

    q_extant().rig_task()
