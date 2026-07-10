import click
import pytest

from pdpp.utils import prompt_helpers


def test_non_interactive_stdin_raises_clean_click_exception(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    def raise_oserror(*args, **kwargs):
        raise OSError(22, "Invalid argument")

    monkeypatch.setattr(prompt_helpers.questionary, "prompt", raise_oserror)

    with pytest.raises(click.ClickException):
        prompt_helpers.prompt_or_abort([{"name": "x"}], "x")


def test_cancelled_prompt_raises_abort(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(prompt_helpers.questionary, "prompt", lambda *a, **k: {})

    with pytest.raises(click.Abort):
        prompt_helpers.prompt_or_abort([{"name": "x"}], "x")


def test_empty_choices_raises_clean_click_exception(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    def raise_valueerror(*args, **kwargs):
        raise ValueError("A list of choices needs to be provided.")

    monkeypatch.setattr(prompt_helpers.questionary, "prompt", raise_valueerror)

    with pytest.raises(click.ClickException):
        prompt_helpers.prompt_or_abort([{"name": "x"}], "x")


def test_valid_response_returned(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(
        prompt_helpers.questionary, "prompt", lambda *a, **k: {"x": "value"}
    )

    assert prompt_helpers.prompt_or_abort([{"name": "x"}], "x") == "value"
