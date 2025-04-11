class UserNotFound(Exception):
    def __init__(self):
        self.add_note("user not found")


class UserInactive(Exception):
    def __init__(self):
        self.add_note("account is disabled")


class InvalidCredentials(Exception):
    def __init__(self):
        self.add_note("invalid credentials")


class EmailInUse(Exception):
    def __init__(self):
        self.add_note("email in use")


class RegistrationNotAllowed(Exception):
    def __init__(self):
        self.add_note("registration not allowed")


class CreateUserError(Exception):
    def __init__(self):
        self.add_note("unable to create user")


class UpdateUserError(Exception):
    def __init__(self):
        self.add_note("unable to update user")


class PasswordRulesError(Exception):
    def __init__(self, message):
        self.add_note(message)


class ActionNotAllowed(Exception):
    def __init__(self):
        self.add_note("action not allowed")
