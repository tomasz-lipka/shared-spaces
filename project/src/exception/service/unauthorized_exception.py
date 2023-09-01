"""
Module containing a custom exception class for service-related errors.
"""
from .service_exception import ServiceException


class UnauthorizedException(ServiceException):
    """
    Custom exception for indicating lack of valid authentication.
    Sub-class of the ServiceException.
    """

    def __init__(self, message):
        self.message = message
        super().__init__(message, 401)
