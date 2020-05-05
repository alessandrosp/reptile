import unittest.mock as mock

import prompt_toolkit.formatted_text as ptk_formatted_text

import reptile
from reptile.forms.input import InputValidator


@mock.patch("prompt_toolkit.prompt", return_value="")
def test_default_is_returned(mock_prompt):
    question = {
        "Type": "Input",
        "Name": "A",
        "Message": "What's the answer?",
        "Default": "42",
    }
    answers = reptile.prompt(question)
    assert answers["A"] == "42"


@mock.patch("prompt_toolkit.prompt", return_value="")
def test_default_is_returned_when_int(mock_prompt):
    question = {
        "Type": "Input",
        "Name": "A",
        "Message": "What's the answer?",
        "Default": 42,
    }
    answers = reptile.prompt(question)
    assert answers["A"] == 42


def test_format_message_returns_pygments_tokens():
    question = {
        "Type": "Input",
        "Name": "A",
        "Message": "What's the answer?",
    }
    form = reptile.FORMS_MAP[question["Type"]](**question)
    assert isinstance(
        form._format_message(), ptk_formatted_text.PygmentsTokens
    )


@mock.patch("prompt_toolkit.prompt", return_value=21)
def test_transform_works(mock_prompt):
    question = {
        "Type": "Input",
        "Name": "A",
        "Message": "What's the answer?",
        "Transform": lambda x: x * 2,
    }
    answers = reptile.prompt(question)
    assert answers["A"] == 42


def test_validator_is_created():
    question = {
        "Type": "Input",
        "Name": "A",
        "Message": "What's the answer?",
        "Validate": lambda x: x == 42,
    }
    form = reptile.FORMS_MAP[question["Type"]](**question)
    # We check that the lambda function has been replaced by
    # an instance of InputValidator.
    assert isinstance(form._validator, InputValidator)
