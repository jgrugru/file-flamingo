from .BaseFile import BaseFile


class TextFile(BaseFile):
    """
    TextFile inherits the BaseFile class. The only
    functionality added is the ability to add text
    to the file and to create the file at the
    the initialization of the class. A user can
    specify the text contents of the file by adding the
    txt key word argument. If the file already exists,
    the txt will be appended to the file.
    """
    def __init__(self, filepath, txt=None):
        super().__init__(str(filepath))
        if txt:
            self.append_text_to_file(txt)

    def get_text_lines_as_list(self):
        """
        Returns all the lines from the text file
        as a list.
        """
        return self.get_contents_of_file().split('\n')

    def append_text_to_file(self, data):
        """
        Creates file if it does not exist and
        appends text to the file. Does not delete
        the file or clear the contents.
        """
        with open(self.filepath, 'a') as f:
            f.write(data)
            f.close()

    def write_text_to_file(self, data):
        """
        Truncates the file and writes the
        data as text.
        """
        with open(self.filepath, 'w') as f:
            f.write(data)
            f.close()

    def append_text_line_to_file(self, file_line):
        self.append_text_to_file(file_line)
        self.append_text_to_file('\n')
