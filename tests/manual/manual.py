"""Manual test module for Reptile.

It requires someone to execute it and follow the instructions that
appear on the various prompts. Note that the same question may appear
multiple times.
"""

import reptile

expected = {
    "checkbox_all": ["A", "B", "C", "D"],
    "checkbox_inverted": ["B", "C", "D"],
    "checkbox_third": ["three"],
    "confirm_n_transform": 0,
    "confirm_y_transform": 1,
    "input_42": "42",
    "input_42_int": 42,
    "input_42_validated": "42",
    "list_first": "A",
    "list_transform": "three",
}
questions = [
    {
        "Type": "Checkbox",
        "Name": "checkbox_all",
        "Message": "Press <a> to select all and press Enter:",
        "Choices": ["A", "B", "C", "D"],
    },
    {
        "Type": "Checkbox",
        "Name": "checkbox_inverted",
        "Message": (
            "Select the first option, press <i> "
            "to invert selections and press Enter:"
        ),
        "Choices": ["A", "B", "C", "D"],
    },
    {
        "Type": "Checkbox",
        "Name": "checkbox_third",
        "Message": "Select the third option and press Enter:",
        "Choices": ["A", "B", "C", "D"],
        "Values": ["one", "two", "three", "four"],
    },
    {
        "Type": "Confirm",
        "Name": "confirm_n_transform",
        "Message": "Press <n>:",
        "Transform": lambda x: 1 if x is True else 0,
    },
    {
        "Type": "Confirm",
        "Name": "confirm_y_transform",
        "Message": "Press <y>:",
        "Transform": lambda x: 1 if x is True else 0,
    },
    {
        "Type": "Input",
        "Name": "input_42",
        "Message": "Type 42 and press Enter:",
    },
    {
        "Type": "Input",
        "Name": "input_42_int",
        "Message": "Type 42 and press Enter:",
        "Transform": lambda x: int(x),
    },
    {
        "Type": "Input",
        "Name": "input_42_validated",
        "Message": "Type 41 and press Enter:",
        "Validate": lambda x: True
        if x == "42"
        else "Delete 41 and type 42 instead.",
    },
    {
        "Type": "List",
        "Name": "list_first",
        "Message": "Select the first element of the list:",
        "Choices": ["A", "B", "C", "D"],
    },
    {
        "Type": "List",
        "Name": "list_transform",
        "Message": "Select the third element of the list:",
        "Choices": ["A", "B", "C", "D"],
        "Values": ["one", "two", "three", "four"],
    },
]
answers = reptile.prompt(questions)

for question_name, expected_answer in expected.items():
    try:
        assert answers[question_name] == expected_answer
    except AssertionError:
        message = "{}: {} != {}".format(
            question_name, expected_answer, answers[question_name]
        )
        raise AssertionError(message)

print("All tests have been passed successfully!")
