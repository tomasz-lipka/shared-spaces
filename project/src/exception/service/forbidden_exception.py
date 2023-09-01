"""
Module containing a custom exception class for service-related errors.
"""
from .service_exception import ServiceException


class ForbiddenException(ServiceException):
    """
    Custom exception for indicating that a resource is not allowed for the user who is requesting it.
    Sub-class of the ServiceException.
    """

    def __init__(self, message):
        self.message = message
        super().__init__(message, 403)
