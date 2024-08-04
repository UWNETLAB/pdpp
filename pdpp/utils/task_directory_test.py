import os
from os.path import isdir, join

import click

from pdpp.utils.rem_slash import rem_slash


class ExistingTaskDirectory(click.types.StringParamType):
    """
    Custom type for directories to check that it is already an existing directory, and
    that it is a proper task directory (meaning it includes input, output,
    and src subdirectories).
    """

    def convert(self, value, param, ctx):
        directory = rem_slash(
            super(ExistingTaskDirectory, self).convert(value, param, ctx)
        )

        if not os.path.isdir(directory):
            raise self.fail(
                (
                    "This directory does not exist.\n"
                    "Please choose an existing task directory."
                ),
                param,
                ctx,
            )

        elif (
            not isdir(join(directory, "src"))
            or not isdir(join(directory, "input"))
            or not isdir(join(directory, "output"))
        ):
            raise self.fail(
                (
                    "This is not a valid task directory.\n"
                    "Please choose an existing task directory "
                    "that you created by running pdpp task."
                ),
                param,
                ctx,
            )

        return directory


class TaskDirectory(click.types.StringParamType):
    """
    Custom type for directories with no spaces, and to ensure that the directory name
    does not already exist. This will keep prompting the user for a proper input type if
    they enter a directory name with spaces or a directory name that already exists.
    """

    def convert(self, value, param, ctx):
        directory = super(TaskDirectory, self).convert(value, param, ctx)

        # Check for spaces
        if " " in directory:
            raise self.fail(
                "\nNo spaces allowed. Please try again.\n", param, ctx
            )  # type: ignore

        # Check for reserved names
        if directory in ["_import_", "_export_"]:
            raise self.fail(
                f"\n'{directory}' is reserved and is not a valid task name. "
                "Please try again.\n",
                param,
                ctx,
            )  # type: ignore

        # Check for lowercase
        if not directory.islower():
            raise self.fail(
                "\nOnly lowercase names are allowed. Please try again.\n", param, ctx
            )  # type: ignore

        # Check if directory already exists
        if os.path.isdir(directory):
            raise self.fail(
                (
                    "\nThis task directory already exists.\n"
                    "Please choose another name for your directory.\n"
                ),
                param,
                ctx,
            )  # type: ignore

        return directory
