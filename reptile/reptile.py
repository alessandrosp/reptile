import typing as t

import prompt_toolkit.styles as ptk_style
from pygments.token import Token as T

from .forms.checkbox import CheckboxForm
from .forms.confirm import ConfirmForm
from .forms.input import InputForm
from .forms.list import ListForm


#  The default style for the various forms. This can be overwritten
#  by passing a new style to the question (key: 'Style').
DEFAULT_STYLE = ptk_style.style_from_pygments_dict(
    {
        #  Style for the answer once it has been submitted.
        T.Answer: "#FF9D00 bold",
        #  Style for the erorr message (validation).
        T.Error: "#E6E5E6 bg:#5F0000",
        #  Style for the instruction snippets.
        T.Instruction: "",
        #  Style used for the cursor (pointer) in MultiForms.
        T.Pointer: "#FF9D00 bold",
        #  Style used for the text in the question.
        T.Question: "bold",
        #  Style for the text prepended to the question (i.e. [?]).
        T.QuestionMark: "#A4F743 bold",
        # Style for the selector (in CheckboxForm).
        T.Selector: "#FF9D00",
    }
)
#  Only the following types are valid questions' types. They each
#  map to a specific form. If a question is asked with a different
#  type an error is raised.
ACCEPTED_TYPES = ["Checkbox", "Confirm", "Input", "List"]
# Map from the string type to the correspondent class.
FORMS_MAP = {
    "Checkbox": CheckboxForm,
    "Confirm": ConfirmForm,
    "List": ListForm,
    "Input": InputForm,
}


class ReptileError(Exception):
    """Basic error for Reptile."""


class UnnamedQuestion(ReptileError):
    """Raised when one of the question doesn't have the field Name."""


class NotUniqueNames(ReptileError):
    """Raised when two or more questions share the same name."""


class InvalidFormType(ReptileError):
    """Raised when the question's type is not included in ACCEPTED_TYPES."""


class MissingFormType(ReptileError):
    """Raised when one of the questions is missing the field Type."""


def prompt(questions: t.Union[list, dict]) -> dict:
    """The primary function the user should interact with.

    It takes some questions (either as a single dict or a list of dicts),
    creates the relevant froms (depending on the key Type) and store
    the responses in the output dict, answers.

    Args:
        questions: The questions to ask, either as a single dict or
            as a list of dicts.

    Returns:
        The answers dict with contains for each question the relevant
        answer. The answers are under a key named after the Name field
        in the relevant question.
    """

    def _check_questions_are_named(questions: t.List[dict]) -> None:
        """Checks that all questions have a Name field."""
        for question in questions:
            if "Name" not in question or not question["Name"]:
                message = "Every question needs to have a Name."
                raise UnnamedQuestion(message)

    def _check_names_are_unique(questions: t.List[dict]) -> None:
        """Checks that all the names across the list of dicts are unique."""
        list_names = [question["Name"].lower() for question in questions]
        set_names = {question["Name"].lower() for question in questions}
        if len(list_names) != len(set_names):
            message = "The questions' names must be unique."
            raise NotUniqueNames(message)

    def _check_valid_form_types(questions: t.List[dict]) -> None:
        """Checks that the various Type used are in ACCEPTED_TYPES."""
        for question in questions:
            if "Type" not in question:
                message = "Questions must specify the type of form to use."
                raise MissingFormType(message)
            if question["Type"] not in ACCEPTED_TYPES:
                message = "The Type selected is not supported."
                raise InvalidFormType(message)

    if isinstance(questions, dict):
        questions = [questions]
    _check_questions_are_named(questions)
    _check_names_are_unique(questions)
    _check_valid_form_types(questions)
    forms = []
    answers = {}
    for question in questions:
        if "Style" not in question or not question["Style"]:
            question["Style"] = DEFAULT_STYLE
        forms.append(FORMS_MAP[question["Type"]](**question))
    for form in forms:
        form.ask_question(answers)
    return answers
