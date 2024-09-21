class IncorrectProfileFormat(Exception):
    def __init__(self, message="Incorrect profile format"):
        self.message = message
        super().__init__(self.message)


class InvalidClient(Exception):
    pass


class InvalidOAuthToken(Exception):
    pass


class ValuesNotMatching(Exception):
    pass
