from os import path, remove, stat, makedirs


class BaseFile():
    """
    Base file class that can be utilized by any
    object that represents a file. The class is
    initialized with a filepath, either relative or
    hardcoded.
    """

    def __init__(self, filepath):
        self.filepath = filepath

    def set_filepath(self, filepath):
        self.filepath = filepath

    def get_filepath(self):
        return self.filepath

    def create_filepath(self):
        """
        Creates filepaths for both dirs and files.
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
        Checks if the filepath exists and that the path
        is not a dir before deleting.
        """
        if self.filepath_exists() and self.is_file():
            remove(self.filepath)
        else:
            print("The file could not be deleted because "
                  + self.filepath + " does not exist or it is a directory.")

    def get_contents_of_file(self):
        """
        Returns all the text read from the file.
        """
        data = None
        with open(self.filepath, 'r') as my_file:
            data = my_file.read()
        return data

    def append_data_to_file(self, data):
        """
        Appends text to the file. Does not delete
        the file or clear the contents.
        """
        with open(self.filepath, 'a') as f:
            f.write(data)
            f.close()

    def write_data_to_file(self, data):
        """
        Truncates the file and writes the
        data as text.
        """
        with open(self.filepath, 'w') as f:
            f.write(data)
            f.close()

    def clear_file(self):
        """
        Checks if the file exists before truncating
        the file. Performs an open, write, close which
        clears all the contents.
        """
        if self.filepath_exists():
            open(self.filepath, 'w').close()
        else:
            print("The file could not be cleared because "
                  + self.filepath + " does not exist.")

    def is_binary(self):
        """
        A simple method to determine if the file
        is not a text file. If UnicodeDecodeError
        is thrown, it is not a text file. In our
        case, we are assuming it is a binary. This
        method is called at the initialization of
        EncryptionFile, so it needs to work when
        the file does not exist, hence the
        FileNotFoundError.
        """
        try:
            with open(self.filepath, "r") as f:
                f.read()
        except UnicodeDecodeError:
            return True
        except FileNotFoundError:
            return False
        return False

    def is_empty(self, verbose_flag=False):
        """
        Returns boolean if size of file is 0.
        """
        if stat(self.filepath).st_size == 0:
            return True
        else:
            return False

    def is_dir(self, verbose_flag=False):
        """
        Utilizes the path(filepath).isdir() function
        from the os module.
        """
        return path.isdir(self.filepath)

    def is_file(self, verbose_flage=False):
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

    def __str__(self):
        return self.filepath
