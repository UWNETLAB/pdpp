import click
from pdpp.utils.rem_slash import rem_slash
import os
from os.path import isdir, join


class ExistingTaskDirectory(click.types.StringParamType):
    """
    Custom type for directories to check that it is already an existing directory, and that it is a proper task directory (meaning it includes input, output, and src subdirectories).
    """

    def convert(self, value, param, ctx):
        directory = rem_slash(super(ExistingTaskDirectory, self).convert(value, param, ctx))

        if directory not in os.listdir():
            raise self.fail("This directory does not exist.\nPlease choose an existing task directory.", param, ctx) # type: ignore

        elif not isdir(join(directory, 'src')) or not isdir(join(directory, 'input')) or not isdir(join(directory, 'output')):
            raise self.fail("This is not a valid task directory.\n"
                            "Please choose an existing task directory that you created by running pdpp task.")# type: ignore

        return directory


class TaskDirectory(click.types.StringParamType):
    """
    Custom type for directories with no spaces, and to ensure that the directory name does not already exist. This will keep prompting the user for a proper input type if they enter a directory name with spaces or a directory name that already exists.
    """

    def convert(self, value, param, ctx):
        directory = super(TaskDirectory, self).convert(value, param, ctx)
        if ' ' in directory:
            raise self.fail("\n No spaces allowed. Please try again. \n", param, ctx) # type: ignore

        if directory == "_import_":
            raise self.fail("\n'_import_' is reserved and is not a valid task name. Please try again. \n", param, ctx) # type: ignore
        
        if directory == "_export_":
            raise self.fail("\n'export' is reserved and is not a valid task name.  Please try again. \n", param, ctx) # type: ignore

        # It appears to already be checking for it all to be lower case, but I'm not sure where..

        if directory in os.listdir():
            raise self.fail("\nThis task directory already exists.\nPlease choose another name for your directory. \n", param, ctx) # type: ignore

        return directory