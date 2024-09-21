class IncorrectMediaProfileFormatInput(Exception):
    pass


class NotSpecifiedClassKwarg(Exception):
    def __init__(self, class_: type, kwarg: str):
        message = self._create_error_message(class_.__name__, kwarg)
        super().__init__(message)

    @staticmethod
    def _create_error_message(class_name: str, kwarg: str):
        return f"Required kwarg={kwarg} of class={class_name} is not specified."
