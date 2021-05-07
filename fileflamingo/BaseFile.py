from os import path, remove, stat, makedirs


class BaseFile():
    """
    Base file class that can be utilized by any
    object that represents a file. The class is
    initialized with a filepath, either relative or
    absolute.
    """

    def __init__(self, filepath):
        self.filepath = filepath
        self.is_encrypted = self.is_binary()

    def set_filepath(self, filepath):
        self.filepath = filepath

    def get_filepath(self):
        return self.filepath

    def create_filepath(self):
        """
        Creates filepath for both dirs and files.
        First creates the directory paths and then tries
        to create the filepath if the filepath is a file.
        """
        tail_head_tuple = path.split(self.filepath)
        if tail_head_tuple[0] == '':
            self.create_file()
        else:
            makedirs(path.dirname(self.filepath), exist_ok=True)
            self.create_file()

    def create_file(self):
        """
        Creates a single file. Will not work
        if there are parent directories or if the filepath
        is a directory.
        """
        try:
            with open(self.filepath, "a") as f:
                f.write("")
        except Exception:
            pass

    def delete_file(self):
        """
        Utilizes the remove method from the os module.
        Only deletes files. If file is not found a
        FileNotFoundError is raised. If the filepath
        is a directory, a IsADirectoryError is raised.
        """
        remove(self.filepath)

    def clear_file(self):
        """
        Utilizes the file truncate() function.
        If file is not found a FileNotFoundError
        is raised. If the filepath is a directory,
        a IsADirectoryError is raised.
        """
        with open(self.filepath, 'r+') as f:
            f.truncate()

    def is_binary(self):
        """
        A method to determine if the file
        is not a text file. If UnicodeDecodeError
        is thrown, it is not a text file. In our
        case, we are assuming it is a binary. This
        method is called at the initialization of
        EncryptionFile, so it needs to work when
        the file does not exist, hence the
        FileNotFoundError. This function will return
        False if the file is a directory.
        """
        try:
            with open(self.filepath, "r") as f:
                f.read()
        except UnicodeDecodeError:
            return True
        except (FileNotFoundError, IsADirectoryError):
            return False
        return False

    def is_empty(self):
        """
        Returns False if size of file is 0.
        If the self.filepath is a directory,
        the stat function returns 4096, which returns
        False.
        """
        if stat(self.filepath).st_size == 0:
            return True
        else:
            return False

    def is_dir(self):
        """
        Utilizes the os.path.isdir() function
        from the os module.
        """
        return path.isdir(self.filepath)

    def is_file(self):
        """
        Utilizes the os.path.isfile() function
        from the os module.
        """
        return path.isfile(self.filepath)

    def filepath_exists(self):
        """
        Returns true if the file is a dir or a file.
        """
        if path.isdir(self.filepath) or path.exists(self.filepath):
            return True
        else:
            return False

    def is_decryptable(self):
        """
        If filepath is a dir, returns False.
        Determines if filepath exists and the file
        is a binary.
        """
        if self.is_dir():
            return False
        else:
            return self.filepath_exists() and self.is_binary()

    def is_encryptable(self):
        """
        If filepath is a dir, returns False.
        Determines if filepath exists and the file is not
        a binary.
        """
        if self.is_dir():
            return False
        else:
            return self.filepath_exists() and not self.is_binary()

    @staticmethod
    def strip_elements_of_list(file_lines):
        """
        Strips each element in list, removing whitespace from
        beginning and end of string.
        """
        return [line.strip() for line in file_lines]

    @staticmethod
    def remove_whitespace_elements(file_lines):
        """
        Remove all elements of list that are only whitespace.
        """
        return list(filter(lambda x: x.strip() != '', file_lines))

    @staticmethod
    def map_file_lines(file_lines, fn):
        """
        Accepts a file_lines list and a function. Creates a new list with
        the contents passed through the funtion (fn).
        """
        return list(map(fn, file_lines))

    def clean_elements_of_whitespace(self, file_lines):
        """
        Removes all unnecessary whitespace from the list.
        Strips each element followed by removing each
        element that is only whitespace.
        """
        file_lines = self.strip_elements_of_list(file_lines)
        file_lines = self.remove_whitespace_elements(file_lines)
        return file_lines

    def __str__(self):
        return self.filepath
