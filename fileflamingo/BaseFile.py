from os import path, remove, stat, makedirs


class BaseFile():
    """
    Base file class that can be utilized by any
    object that represents a file. Contains
    functions:
    get_contents_of_file (only works with text),
    create_filepath (either a file or a dir),
    delete_file (only works on files, not dirs),
    append_data_to_file,
    write_data_to_file,
    clear_file,
    is_binary,
    is_empty,
    is_dir,
    is_file,
    filepath_exists.
    """

    def __init__(self, filepath):
        self.filepath = filepath

    def set_filepath(self, filepath):
        self.filepath = filepath

    def get_filepath(self):
        return self.filepath

    def create_filepath(self, verbose_flag=False):
        makedirs(path.dirname(self.filepath), exist_ok=True)
        try:
            with open(self.filepath, "a") as f:
                f.write("")
        except Exception:
            pass

    def delete_file(self):
        if self.filepath_exists() and self.is_file():
            remove(self.filepath)
        else:
            print("The file could not be deleted because "
                  + self.filepath + " does not exist or it is a directory.")

    def get_contents_of_file(self):
        data = None
        with open(self.filepath, 'r') as my_file:
            data = my_file.read()
        return data

    def append_data_to_file(self, data):
        with open(self.filepath, 'a') as f:
            f.write(data)
            f.close()

    def write_data_to_file(self, data):
        with open(self.filepath, 'w') as f:
            f.write(data)
            f.close()

    def clear_file(self, verbose_flag=False):
        if self.filepath_exists():
            open(self.filepath, 'w').close()
            if verbose_flag:
                print("Cleared the contents of " + self.filepath)
        else:
            print("The file could not be cleared because "
                  + self.filepath + " does not exist.")

    def is_binary(self, verbose_flag=False):
        try:
            with open(self.filepath, "r") as f:
                f.read()
        except UnicodeDecodeError:
            return True
        except FileNotFoundError:
            return False
        return False

    def is_empty(self, verbose_flag=False):
        if stat(self.filepath).st_size == 0:
            return True
        else:
            return False

    def is_dir(self, verbose_flag=False):
        return path.isdir(self.filepath)

    def is_file(self, verbose_flage=False):
        return path.isfile(self.filepath)

    def filepath_exists(self):
        if path.isdir(self.filepath) or path.exists(self.filepath):
            return True
        else:
            return False

    def __str__(self):
        return self.filepath
