import typing as t

import prompt_toolkit as ptk
import prompt_toolkit.document as ptk_document
import prompt_toolkit.formatted_text as ptk_formatted_text
import prompt_toolkit.validation as ptk_validation
from pygments.token import Token as T

from .abstract import AbstractForm


class InputValidator(ptk_validation.Validator):
    """Validator wrapper for InputForms.

    The prompt() in InputForms accept a ptk_validation.Validator as
    argument for validation (which means we don't need to rely on
    custom-made solutions). Thus, the function provided by the user
    is wrapped in a InputValidator. The usual applies: if the
    function returns True, the input is validated. If False or str,
    the validation fails (if str, then the string is used as the
    message to display to the user).

    Args:
        function: The function to use for validation.
    """

    def __init__(self, function: t.Callable[[str], t.Union[bool, str]]):
        self._function = function

    def validate(self, document: ptk_document.Document) -> None:
        """Validates the content inputted by the user."""
        validation = self._function(document.text)
        cursor_position = len(document.text)

        message = ""
        if not validation:
            message = "The input was not validated succesfully."
        if isinstance(validation, str):
            message = validation
        if message:
            raise ptk_validation.ValidationError(
                message=message, cursor_position=cursor_position
            )


class InputForm(AbstractForm):
    """Class for forms of type Input.

    InputForms are forms where the user is asked to type some input
    following a question, e.g. [?] What's your name?
    """

    def __init__(self, **kwargs: dict) -> None:
        super(InputForm, self).__init__(**kwargs)
        if self._validate:
            self._validator = InputValidator(self._validate)
        else:
            self._validator = None

    def _format_message(self) -> ptk_formatted_text.PygmentsTokens:
        """Formats the message provided by the user to improve readability."""
        message_tokens = [
            (T.QuestionMark, "[?] "),
            (T.Question, self._message + " "),
        ]
        message_fragments = ptk_formatted_text.PygmentsTokens(message_tokens)
        return message_fragments

    def _ask_question(self, answers: dict) -> None:
        answers[self._name] = ptk.prompt(
            self._format_message(),
            style=self._style,
            validator=self._validator,
            validate_while_typing=False,
        )
