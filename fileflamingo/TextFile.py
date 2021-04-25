from .BaseFile import BaseFile


class TextFile(BaseFile):

    def __init__(self, filepath, txt=None):
        super().__init__(str(filepath))
        if txt:
            self.append_text_to_file(txt)
