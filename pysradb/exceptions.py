"""This file contains custom Exceptions for pysradb"""


class MissingQueryException(Exception):
    """Exception raised when the user did not supply any query fields.

    Attributes:
        message: string
            Error message for this Exception

    """

    def __init__(self):
        raise NotImplementedError


class IncorrectFieldException(Exception):
    """Exception raised when the user enters incorrect inputs for a flag."""

    pass
