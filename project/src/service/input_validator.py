"""
Module for input validation functions. This module provides a set of 
functions for validating user input, ensuring that it meets certain criteria.
"""
from ..exception.service_exception import ServiceException

MIN_LEN = 3


def validate_usr_input(usr_input, field_name, max_len):
    """
    Validate user input for a specific field.
    Args:
        usr_input (str): The user input to be validated.
        field_name (str): The name of the field being validated (for error messages).
        max_len (int): The maximum allowed characters length for the string input.
    Returns:
        bool: True if the input is valid, False otherwise.
    """
    usr_input = str(usr_input)
    __validate_max_len(usr_input, field_name, max_len)
    __validate_min(usr_input, field_name)
    __valdiate_empty(usr_input, field_name)


def __validate_max_len(usr_input, field_name, max_len):
    if len(usr_input) > max_len:
        raise ServiceException(f"{field_name} max {max_len} characters")


def __validate_min(usr_input, field_name):
    if len(usr_input) < MIN_LEN:
        raise ServiceException(f"{field_name} min {MIN_LEN} characters")


def __valdiate_empty(usr_input, field_name):
    if usr_input.isspace():
        raise ServiceException(f"{field_name} cannot be empty")
