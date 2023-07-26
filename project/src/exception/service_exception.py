class ServiceException(Exception):
    """Custom exception class for errors occuring in the service layer"""

    def __init__(self, message):
        self.message = message
        super().__init__(message)
