from os import path, remove, stat, makedirs
from .BaseFile import BaseFile

class EncryptionFile():
    """
    Base file class inherited by EnvDir, EnvFile,
    PemFile. Contains functions that can be utilized by any file.
    """

    def get_contents_of_file(self):
        if not self.is_binary():
            data = self.get_contents_of_text_file()
        else:
            data = self.get_contents_binary_file()
        return data

    def get_contents_of_text_file(self):
        data = None
        with open(self.filepath, 'r') as my_file:
            data = my_file.read()
        return data

    def get_contents_binary_file(self):
        data = None
        with open(self.filepath, 'rb') as my_file:
            data = my_file.read()
        return data

    def write_data_to_file(self, data, verbose_flag=False):
        self.clear_file()

        if not self.is_binary():
            self.write_data_to_binary(data, verbose_flag)
        else:
            self.write_data_to_text(data, verbose_flag)

    def write_data_to_binary(self, data, verbose_flag):
        with open(self.filepath, 'wb') as env_file:
            env_file.write(data)
            env_file.close()
        if verbose_flag:
            print("Wrote encrypted data to " + str(self))

    def write_data_to_text(self, data, verbose_flag):
        with open(self.filepath, 'w') as env_file:
            env_file.write(data)
            env_file.close()
        if verbose_flag:
            print("Wrote decrypted data to " + str(self))
