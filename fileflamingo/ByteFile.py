from .BaseFile import BaseFile

line_separator = b'aJh@WDFWDg-#4jZr'

 
class ByteFile(BaseFile):
    """
    ByteFile inherits from the base BaseFile class.
    This class can be used to represent
    a binary file. The functions in the class
    allow the user to read/write bytes to the file.
    """
    def __init__(self, filepath):
        super().__init__(str(filepath))

    def write_bytes_to_file(self, data):
        """
        Writes data to the file as bytes.
        """
        with open(self.filepath, 'wb') as env_file:
            env_file.write(data)

    def append_byte_line_to_file(self, file_line):
        """
        Appends bytes to the file followed by
        the line_separator.
        """
        self.append_bytes_to_file(file_line)
        self.append_bytes_to_file(line_separator)

    def append_bytes_to_file(self, data):
        """
        Appends data to the file as bytes.
        Creates file if it does not exist.
        """
        with open(self.filepath, 'ab+') as env_file:
            env_file.write(data)

    def get_bytes_from_file(self):
        """
        Returns the bytes read from the file.
        """
        with open(self.filepath, 'rb') as my_file:
            data = my_file.read()
        return data

    def get_byte_lines_as_list(self):
        """
        Returns a list of bytes in the file
        split at the line_separator.
        """
        return self.get_bytes_from_file().split(line_separator)
