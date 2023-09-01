"""
Module containing a custom exception class for service-related errors.
"""
from .service_exception import ServiceException


class NotFoundException(ServiceException):
    """
    Custom exception for indicating that a resource or item was not found.
    Sub-class of the ServiceException.
    """

    def __init__(self, message):
        self.message = message
        super().__init__(message, 404)
