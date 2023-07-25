class RepositoryException(Exception):
    """
    Custom exception class for exceptions occuring in the repository layer
    """

    def __init__(self, message):
        self.message = message
        super().__init__(message)
