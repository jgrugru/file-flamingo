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
