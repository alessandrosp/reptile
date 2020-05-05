import prompt_toolkit as ptk
import prompt_toolkit.formatted_text as ptk_formatted_text
import prompt_toolkit.keys as ptk_keys
from pygments.token import Token as T

from .input import InputForm


class ConfirmForm(InputForm):
    """A form where the user is asked to confirm with a Yes/No question.

    This form is a more specific version of InputForm, one where pressing
    one between Y, y, N and n will immediately stop the prompt and
    store either a True or False into answers.
    """

    def __init__(self, **kwargs):
        super(ConfirmForm, self).__init__(**kwargs)
        self._add_key_bindings()

    def _add_key_bindings(self) -> None:
        """Adds keys to self.__key_bindings for y/N confirmation."""

        @self._key_bindings.add("y")
        @self._key_bindings.add("Y")
        def yes(event) -> None:
            event.current_buffer.text = "y"
            event.app.exit(result=True)

        @self._key_bindings.add("n")
        @self._key_bindings.add("N")
        def no(event) -> None:
            event.current_buffer.text = "n"
            event.app.exit(result=False)

        @self._key_bindings.add(ptk_keys.Keys.Any)
        def _(event) -> None:
            """Disallows inserting other text."""
            pass

    def _format_message(self) -> ptk_formatted_text.PygmentsTokens:
        message_fragments = super(ConfirmForm, self)._format_message()
        instructions_tokens = [(T.Instruction, "(y/n) ")]
        message_fragments.token_list += instructions_tokens
        return message_fragments

    def _ask_question(self, answers: dict) -> None:
        answers[self._name] = ptk.prompt(
            self._format_message(),
            style=self._style,
            validate_while_typing=False,
            key_bindings=self._key_bindings,
        )
