"""
Module containing a custom exception class for service-related errors.
"""
from service_exception import ServiceException

class NotFoundException(ServiceException):


    def __init__(self, message):
        self.message = message
        super().__init__(message)
