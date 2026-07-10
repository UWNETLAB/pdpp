"""Wrappers that turn questionary prompt failures into clean CLI exits.

pdpp's interactive prompts previously indexed the questionary result dict
directly (``prompt(...)["key"]``). That crashed with a raw traceback in two
common situations:

- the user pressed Ctrl-C, so questionary returned ``{}`` and the index raised
  ``KeyError``; and
- stdin was not a TTY (a pipe, or CI), so prompt_toolkit raised
  ``OSError [Errno 22]``.

``prompt_or_abort`` centralizes both cases: a cancel becomes ``click.Abort``
(clean exit code 1, no traceback) and a non-interactive stdin becomes a
``click.ClickException`` with an actionable message.
"""

from typing import Any, List

import click
import questionary

from pdpp.styles.prompt_style import custom_style_fancy


def prompt_or_abort(questions: List[dict], key: str) -> Any:
    """Run a questionary prompt and return ``result[key]``.

    Raises ``click.ClickException`` when stdin is not interactive and
    ``click.Abort`` when the user cancels the prompt.
    """
    try:
        result = questionary.prompt(questions, style=custom_style_fancy)
    except OSError as exc:
        raise click.ClickException(
            "This command needs an interactive terminal. It cannot be run with "
            "piped or redirected input."
        ) from exc
    except ValueError as exc:
        # questionary raises ValueError when a prompt has no choices to offer,
        # e.g. a project with nothing to rig or enable.
        raise click.ClickException(
            "There is nothing available to select for this command in the "
            "current project."
        ) from exc

    if not result or key not in result:
        raise click.Abort()

    return result[key]
