"""
Module containing a custom exception class for service-related errors.
"""


class ServiceException(Exception):
    """
    This exception is raised to indicate errors that occur in the service layer
    of the application. It allows attaching a custom error message to provide more
    context about the error.

    Args:
        message (str): The error message describing the reason for the exception.
        error_code (int): An error code associated with the exception.
    """

    def __init__(self, message, error_code):
        self.message = message
        self.error_code = error_code
        super().__init__(message)
