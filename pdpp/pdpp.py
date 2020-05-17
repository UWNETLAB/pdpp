from pdpp.src.utils.ExistingStepFolder import ExistingStepFolder, StepFolder
import click
 
CONTEXT_SETTINGS = dict(help_option_names=['-h', '--help'])
files_list = ['png', 'pdf', 'both']

@click.group()
def main():
    """A command line tool to automate the use of the Principled Data Processing methodology for reproducibility."""
    pass

# rig
@main.command(short_help="Incorporates a step in the project's automation")
def rig():
    from pdpp.src.rig import rig as rig_step
    rig_step()

 
# graph
@main.command(short_help="Creates a dependency graph to visualize how the steps in your project relate "
                         "to each other.", context_settings=CONTEXT_SETTINGS)
@click.option('--files', '-f',
              type=click.Choice(files_list),
              prompt="What file format would you prefer as an output?",
              help="The dependency graph can be outputted in either .png or .pdf formats. Default is to output .pdf format.",
              default="pdf")
def graph(files):
    from pdpp.src.graph_dependencies import depgraph
    """Creates a dependency graph to visualize how the steps in your project relate to each other."""
    depgraph(files)


# run
@main.command(short_help="Runs the project")
def run():
    from pdpp.src.doit_constructors.doit_run import doit_run
    doit_run()

# select
@main.command(short_help="Selects which tasks will resolve when pdpp run is called")
def select():
    from pdpp.src.task_enabler import task_enabler
    task_enabler()


# new
@main.command(short_help="Creates a new directory named <dirname>, with subdirectories 'input', "
                         "'output', and 'src'. Adds dodo.py to <dirname>. Use this to create a new step folder. "
                         "You will be asked to indicate which other steps are dependencies of this step,"
                         "And which files from those steps should be immediately linked to the new step.",
              context_settings=CONTEXT_SETTINGS)
@click.option('--dirname', '-s',
              type=StepFolder(),
              prompt="What do you want to call the new task directory?\n"
                     "(Use all lower case and separate words with an underscore)",
              help="This is what you want to name your new step folder. "
                   "It must be all lower case and contain no spaces."
              )
def new(dirname):
    """Creates a new directory named <dirname>, with subdirectories 'input', 'output', and 'src'.
    Adds dodo.py to <dirname>. Use this to create a new step folder."""
    from pdpp.src.create_new_task import create_new_task

    from pdpp.src.utils.rem_slash import rem_slash
    create_new_task(rem_slash(dirname))
    click.echo(f"Your new step folder, {dirname}, was created.")



# @main.command(short_help="Creates a dependency graph to visualize how the steps in your project relate "
#                          "to each other.", context_settings=CONTEXT_SETTINGS)
# @click.option('--files', '-f',
#               type=click.Choice(files_list),
#               prompt="What file format would you prefer as an output?",
#               help="The dependency graph can be outputted in either .png or .pdf formats. Default is to output .pdf format.",
#               default="pdf")
# def graph(files):
#     """Creates a dependency graph to visualize how the steps in your project relate to each other."""
#     depgraph(files)
