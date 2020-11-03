import click
from pdpp.utils.rem_slash import rem_slash
import os
from os.path import isdir, join


class ExistingStepFolder(click.types.StringParamType):
    """
    Custom type for folders to check that it is already an existing folder, and that it is a proper step folder (meaning it includes input, output, and src subdirectories).
    """

    def convert(self, value, param, ctx):
        folder = rem_slash(super(ExistingStepFolder, self).convert(value, param, ctx))

        if folder not in os.listdir():
            raise self.fail("This folder does not exist.\nPlease choose an existing step folder.", param, ctx) # type: ignore

        elif not isdir(join(folder, 'src')) or not isdir(join(folder, 'input')) or not isdir(join(folder, 'output')):
            raise self.fail("This is not a valid step folder.\n"
                            "Please choose an existing step folder that you created by running pdpp step.")# type: ignore

        return folder


class StepFolder(click.types.StringParamType):
    """
    Custom type for folders with no spaces, and to ensure that the folder name does not already exist. This will keep prompting the user for a proper input type if they enter a folder name with spaces or a folder name that already exists.
    """

    def convert(self, value, param, ctx):
        folder = super(StepFolder, self).convert(value, param, ctx)
        if ' ' in folder:
            raise self.fail("\n No spaces allowed. Please try again. \n", param, ctx) # type: ignore

        if folder == "_import_":
            raise self.fail("\n'_import_' is reserved and is not a valid step name. Please try again. \n", param, ctx) # type: ignore
        
        if folder == "_export_":
            raise self.fail("\n'export' is reserved and is not a valid step name.  Please try again. \n", param, ctx) # type: ignore

        # It appears to already be checking for it all to be lower case, but I'm not sure where..

        if folder in os.listdir():
            raise self.fail("\nThis step folder already exists.\nPlease choose another name for your folder. \n", param, ctx) # type: ignore

        return folder