import prompt_toolkit.application as ptk_app
import prompt_toolkit.layout.containers as ptk_containers
import prompt_toolkit.layout.layout as ptk_layout

from .multi import MultiForm


class ListForm(MultiForm):
    """Class for forms of type List.

    ListForms are forms where the user is presented with a series of
    Choices and can only select one of these options. If Values is specified
    then the corresponding value of Values is stored in the answers dict,
    otherwise Choices is used instead.

    Note that ListForms do not implement any validation mechanisms, so
    even if you pass a function nothing will happen. That's because
    the Choices are limited and decided by whoever created the form.
    """

    def __init__(self, **kwargs: dict) -> None:
        super(ListForm, self).__init__(**kwargs)
        self._add_key_bindings()

    def _add_key_bindings(self) -> None:
        """Adds keys to self.__key_bindings for list movements."""

        @self._key_bindings.add("enter")
        def enter(event: object) -> None:
            event.app.exit()

    def _ask_question(self, answers: dict) -> None:
        """Asks a question and store the answer in the answers dict."""
        instructions = "(Use arrow keys)"
        self._question_window = self._generate_question_window(instructions)
        self._choices_windows = self._generate_choices_windows("List")
        windows = [self._question_window] + self._choices_windows
        body = ptk_containers.HSplit(windows)
        application = ptk_app.Application(
            layout=ptk_layout.Layout(body),
            key_bindings=self._key_bindings,
            full_screen=False,
            style=self._style,
        )
        application.run()
        answers[self._name] = self._values[self._idx_cursor]
