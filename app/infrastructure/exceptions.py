class UserNotFound(Exception):
    pass


class PasswordError(Exception):
    def __init__(self, message):
        self.message = message
