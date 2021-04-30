line_separator = b'aJh@WDFWDg-#4jZr'


class ByteFile():
    def __init__(self, filepath):
        super().__init__(str(filepath))

    def write_bytes_to_file(self, data):
        """
        Writes data to the file as bytes.
        """
        if self.filepath_exists():
            with open(self.filepath, 'wb') as env_file:
                env_file.write(data)
                env_file.close()
        else:
            print(self.get_filepath() + " does not exist.")

    def write_byte_line_to_file(self, file_line):
        """
        Writes bytes to the file followed by
        the line_separator.
        """
        self.append_bytes_to_file(file_line)
        self.append_bytes_to_file(line_separator)

    def append_bytes_to_file(self, data):
        """
        Appends data to the file as bytes.
        Creates file if it does not exist.
        """
        if self.filepath_exists():
            with open(self.filepath, 'ab') as env_file:
                env_file.write(data)
                env_file.close()
        else:
            print(self.get_filepath() + " does not exist.")

    def get_bytes_from_file(self):
        """
        Returns the bytes read from the file.
        """
        data = None
        with open(self.filepath, 'rb') as my_file:
            data = my_file.read()
        return data

    def get_lines_as_list_from_byte_file(self):
        """
        Returns a list of bytes in the file
        split at the line_separator.
        """
        return self.get_bytes_from_file().split(line_separator)
