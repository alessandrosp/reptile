import typing as t

import prompt_toolkit.application as ptk_app
import prompt_toolkit.formatted_text as ptk_formatted_text
import prompt_toolkit.layout.containers as ptk_containers
import prompt_toolkit.layout.controls as ptk_controls
from pygments.token import Token as T

from .abstract import AbstractForm


class MultiForm(AbstractForm):
    """Parent class for forms that presents multiple options to choose from.

    Both ListForm and CheckboxForm are children of this class. This parent
    class implements a few comodity functions such as vertical movements
    for the cursor.
    """

    #  Parent class for Checkbox and Listform.
    def __init__(self, **kwargs: dict) -> None:
        super(MultiForm, self).__init__(**kwargs)
        self._idx_cursor = 0
        self._add_cursor_key_bindings()

    def _add_cursor_key_bindings(self) -> None:
        """Adds keys to self.__key_bindings for up/down movements."""

        @self._key_bindings.add("up")
        def move_cursor_up(event: object) -> None:
            self._move_cursor_up(event.app)

        @self._key_bindings.add("down")
        def move_cursor_down(event: object) -> None:
            self._move_cursor_down(event.app)

    def _unset_cursor(self, window: ptk_containers.Window) -> None:
        """Removes the cursor pointer from a given window."""
        token = (T.Pointer, "  ")
        window.content.text.token_list[0] = token

    def _set_cursor(self, window: ptk_containers.Window) -> None:
        """Adds the cursor pointer to a given window."""
        token = (T.Pointer, "❯ ")
        window.content.text.token_list[0] = token

    def _move_cursor_up(self, application: ptk_app.Application) -> None:
        """Moves the cursor from one window to the one above.

        The cursor is removed from the "active" window (self._idx_cursor
        is used to keep track of which window is active) and added to
        the one above it.
        """
        #  If the cursor is already at first position, then
        #  we don't do anything and simply return None.
        if self._idx_cursor == 0:
            return None
        self._unset_cursor(self._choices_windows[self._idx_cursor])
        self._set_cursor(self._choices_windows[self._idx_cursor - 1])
        self._idx_cursor -= 1

    def _move_cursor_down(self, application: ptk_app.Application) -> None:
        """Moves the cursor from one window to the one below.

        The cursor is removed from the "active" window (self._idx_cursor
        is used to keep track of which window is active) and added to
        the one below it.
        """
        #  If the cursor is already at last position, then
        #  we don't do anything and simply return None.
        max_idx = len(self._choices) - 1
        if self._idx_cursor == max_idx:
            return None
        self._unset_cursor(self._choices_windows[self._idx_cursor])
        self._set_cursor(self._choices_windows[self._idx_cursor + 1])
        self._idx_cursor += 1

    def _generate_question_window(
        self, instructions: str
    ) -> ptk_containers.Window:
        """Generates a Window for the question and instructions."""
        question_tokens = [
            (T.QuestionMark, "[?] "),
            (T.Question, self._message),
            (T.Instruction, " {}".format(instructions)),
        ]
        question_fragments = ptk_formatted_text.PygmentsTokens(question_tokens)
        question_text = ptk_controls.FormattedTextControl(
            question_fragments, show_cursor=False
        )
        return ptk_containers.Window(question_text, height=1)

    def _generate_choices_windows(
        self, form_type: str
    ) -> t.List[ptk_containers.Window]:
        """Generates a list of Windows for the various Choices."""
        assert form_type in ("List", "Checkbox")
        tokens_groups = []
        #  First, each choice is transformed into a Pygments' Token. These
        #  tokens are not supported natively in prompt_toolkit anymore, so
        #  they need to be transformed via PygmentsTokens().
        for idx, choice in enumerate(self._choices):
            tokens = [(T.Pointer, "❯ ")] if idx == 0 else [(T.Pointer, "  ")]
            if form_type == "Checkbox":
                tokens.append((T.Selector, "○ "))
            tokens.append((T.Text, choice))
            tokens_groups.append(tokens)
        fragments_groups = [
            ptk_formatted_text.PygmentsTokens(tokens)
            for tokens in tokens_groups
        ]
        texts = [
            ptk_controls.FormattedTextControl(fragments, show_cursor=False)
            for fragments in fragments_groups
        ]
        return [ptk_containers.Window(text, height=1) for text in texts]
