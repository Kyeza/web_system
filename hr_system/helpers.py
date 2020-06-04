class Error(Exception):
    """Base class for exceptions in this module."""
    pass


class ProcessingDataError(Error):
    """Exception raised for errors while processing payroll.

    Attributes:
        exception -- input expression in which the error occurred
        user -- explanation of the error
    """

    def __init__(self, user, exception=None, line_number=None):
        self.user = user
        self.exception = exception
        self.line_number = line_number
