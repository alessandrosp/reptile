import prompt_toolkit.application as ptk_app
import prompt_toolkit.formatted_text as ptk_formatted_text
import prompt_toolkit.layout.containers as ptk_containers
import prompt_toolkit.layout.controls as ptk_controls
import prompt_toolkit.layout.layout as ptk_layout

from pygments.token import Token as T

from .multi import MultiForm


class CheckboxForm(MultiForm):
    """Form for when the user can select multiple options from Choices.

    This form is different from ListForm in that the user can select
    multiple options. As such, the answer is stored as a list().
    """

    def __init__(self, **kwargs: dict) -> None:
        super(CheckboxForm, self).__init__(**kwargs)
        self._selected = set()
        self._add_key_bindings()

    def _add_key_bindings(self) -> None:
        """Adds keys to self.__key_bindings for list movements."""

        @self._key_bindings.add("enter")
        def enter(event: object) -> None:
            self._selection = [self._values[s] for s in sorted(self._selected)]
            validation = (
                self._validate(self._selection) if self._validate else True
            )
            if validation is True:
                event.app.exit()
            else:
                message = "Could not validate the input succesfully."
                if isinstance(validation, str):
                    message = validation
                self._display_error(message)

        @self._key_bindings.add("space")
        def click(event: object) -> None:
            if self._idx_cursor not in self._selected:
                self._selected.add(self._idx_cursor)
                self._select(self._choices_windows[self._idx_cursor])
            else:
                self._selected.remove(self._idx_cursor)
                self._deselect(self._choices_windows[self._idx_cursor])

        @self._key_bindings.add("a")
        def select_all(event: object) -> None:
            for idx in range(len(self._choices_windows)):
                self._selected.add(idx)
                self._select(self._choices_windows[idx])

        @self._key_bindings.add("i")
        def invert_all(event: object) -> None:
            for idx in range(len(self._choices_windows)):
                if idx not in self._selected:
                    self._selected.add(idx)
                    self._select(self._choices_windows[idx])
                else:
                    self._selected.remove(idx)
                    self._deselect(self._choices_windows[idx])

    def _select(self, window: ptk_containers.Window) -> None:
        """Marks a given choice as selected."""
        token = (T.Selector, "● ")
        window.content.text.token_list[1] = token

    def _deselect(self, window: ptk_containers.Window) -> None:
        """Marks a given choice as deselected."""
        token = (T.Selector, "○ ")
        window.content.text.token_list[1] = token

    def _display_error(self, message: str) -> None:
        """Displays an error message in a dedicated Window.

        This is used when the validation fails to notify the user.

        Args:
            message: The message to display the user.
        """
        token = (T.Error, message)
        self._error_window.content.text.token_list[0] = token
        self._error_window.height = 1

    def _generate_error_window(self):
        """Generates an empty error Window for later use."""
        #  Note that because the height is 0 by default, this window
        #  will not be visible unless the height is changed.
        empty_tokens = [(T.Error, "")]
        empty_fragments = ptk_formatted_text.PygmentsTokens(empty_tokens)
        empty_text = ptk_controls.FormattedTextControl(
            empty_fragments, show_cursor=False
        )
        return ptk_containers.Window(empty_text, height=0)

    def _ask_question(self, answers: dict) -> None:
        """Asks a question and store the answer in the answers dict."""
        instructions = (
            "(<up>, <down> to move, <space> to select, "
            "<a> to select all, <i> to invert all)"
        )
        self._question_window = self._generate_question_window(instructions)
        self._choices_windows = self._generate_choices_windows("Checkbox")
        self._error_window = self._generate_error_window()
        windows = (
            [self._question_window]
            + self._choices_windows
            + [self._error_window]
        )
        body = ptk_containers.HSplit(windows)
        application = ptk_app.Application(
            layout=ptk_layout.Layout(body),
            key_bindings=self._key_bindings,
            full_screen=False,
            style=self._style,
        )
        application.run()
        answers[self._name] = self._selection
