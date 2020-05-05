import abc
import collections

import prompt_toolkit.key_binding as ptk_key_binding


class AbstractForm(abc.ABC):
    """Abstract class for all the other Reptile forms.

    Args:
        kwargs: A dictionary containg all the information necessary to
            instantie the form. Specifically:
            - Name: The name of the question being asked. This acts as a
                unique identifier for the question. These names will be
                then used as key for the answers dictionary. This field
                is mandatory.
            - Message: The message to display with the question, it's
                normally the question itself. This field is currently
                mandatory.
            - Choices: An array-like structure of values to display to
                the user. Only relevant for list-like forms such as ListForm.
                Optional for certain forms and required for others.
            - Values: An array-like structure with the same lenght as Choices.
                If specified (it's entirely optional), it provides
                backend values for Choices. If the user select the second
                value in Choices within the form, then the final
                dictionary will store the second element of Values. If
                Values is not specified, then Choices is used instead.
            - Validate: A function to use to validate the data. These
                function can return True (valid), False (invalid with
                generic message) or a str (invalid, the string is used
                as error message). Note that some forms may not use
                Validate even when provided (e.g., ListForm).
            - Transform: A function that takes the input provided
                by the user and transform it into something else. Assuming
                the value provided by the user is x, the final answers dict
                will contain Transfom(x) instead of x.
            - When: A function that takes the whole answers dict (before
                the specific question is asked) and return either True or
                False. If True, the question is asked, if False skipped.
                This is useful if you want to have a series of questions
                with some of them being conditional.
    """

    def __init__(self, **kwargs: dict) -> None:
        k = collections.defaultdict(lambda: None, kwargs)
        self._name = k["Name"]
        self._message = k["Message"]
        self._choices = k["Choices"]
        self._validate = k["Validate"]
        self._transform = k["Transform"]
        self._when = k["When"]
        self._style = k["Style"]
        #  If no Values are passed, self._values default to Choices
        #  if Choices is actually available.
        self._values = k["Values"] if k["Values"] else k["Choices"]
        if self._values:
            assert len(self._values) == len(self._choices)
        if "Default" in k:
            #  If Default is not defined, then self._default is not
            #  specified. The reason we don't assign None to it is that the
            #  user may want to specify None as a default value and we want
            #  to be able to respect that.
            self._default = k["Default"]
        self._generate_key_bindings()

    def _generate_key_bindings(self) -> None:
        """Generates a KeyBindings() object and store it internally.

        Children classes can then directly add keys to the self._key_bindings
        via the apposite decorator @self._key_bindings.add().
        """
        self._key_bindings = ptk_key_binding.KeyBindings()

    @abc.abstractmethod
    def _ask_question(self, answers: dict) -> None:
        """Asks the question and stores the answer in the dict.

        This method is an abstract ABC method, which means it has to be
        overridden by the child class before any object can be instantiated.

        Args:
            answers: the dict where to store the answers.
        """
        pass

    def ask_question(self, answers: dict) -> None:
        """Asks the question and stores the answer in the dict.

        This is the only method that should be public in a form and it
        should never be overriden. On top of asking a question, it
        checks whether the question should be asked (the When), it provides
        a default value if one is specified, etc.

        Args:
            answers: the dict where to store the answers.
        """
        if not self._when or self._when(answers):
            self._ask_question(answers)
            if not answers[self._name] and hasattr(self, "_default"):
                answers[self._name] = self._default
            if self._transform:
                answers[self._name] = self._transform(answers[self._name])
