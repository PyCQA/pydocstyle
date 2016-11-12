"""Custom exceptions."""


class IllegalConfiguration(Exception):
    """An exception for illegal configurations."""
    pass


class InvalidErrorFormat(IllegalConfiguration):
    """An execption for an invalid error format string."""
    pass
