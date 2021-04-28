from os import path, remove, stat, makedirs


class BaseFile():
    """
    Base file class that can be utilized by any
    object that represents a file. The class is
    initialized with a filepath, either relative or
    absolute.
    """

    def __init__(self, filepath):  # add a parameter that accepts
        self.filepath = filepath   # and adds contents to file.
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
        makedirs(path.dirname(self.filepath), exist_ok=True)
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

    def get_contents_of_file(self):
        """
        Returns all the text read from the file.
        If the file is not text, it will return
        UnicodeDecodeError.
        """
        data = None
        with open(self.filepath, 'r') as my_file:
            data = my_file.read()
        return data

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
        True.
        """
        if stat(self.filepath).st_size == 0:
            return True
        else:
            return False

    def is_dir(self):
        """
        Utilizes the path(filepath).isdir() function
        from the os module.
        """
        return path.isdir(self.filepath)

    def is_file(self):
        """
        Utilizes the path(filepath).isfile() function
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
            return self.filepath_exists() and self.is_encrypted

    def is_encryptable(self):
        """
        If filepath is a dir, returns False.
        Determines if filepath exists and the file is not
        a binary.
        """
        if self.is_dir():
            return False
        else:
            return self.filepath_exists() and not self.is_encrypted

    def __str__(self):
        return self.filepath
