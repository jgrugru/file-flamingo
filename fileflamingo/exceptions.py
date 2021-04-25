class CannotDeleteDirectoryError(Exception):
    """
    Exception raised when the filepath is a directory
    and is trying to be deleted or cleared.
    """

    def __init__(self,
                 filepath,
                 message="Filepath is a directory, not a file."):
        self.filepath = filepath
        self.message = message
        super().__init__(self.message)
