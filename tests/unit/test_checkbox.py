import unittest.mock as mock

import prompt_toolkit.application as ptk_app

import reptile


@mock.patch.object(ptk_app, "Application")
def test_default_is_returned(mock_app):
    question = {
        "Type": "Checkbox",
        "Name": "A",
        "Message": "What's the answer?",
        "Choices": ["A", "B", "C"],
        "Default": "42",
    }
    form = reptile.FORMS_MAP[question["Type"]](**question)
    form._selection = []
    answers = {}
    form.ask_question(answers)
    assert answers["A"] == "42"
