from .BaseFile import BaseFile
from .Encryptor import Encryptor

line_separator = b'aJh@WDFWDg-#4jZr'


class EncryptionFile(BaseFile):
    """
    EncryptionFile class inherits from BaseFile. EncryptionFile allows you to
    encrypt and decrypt the contents of the file. Constructor requires a
    filepath to an RSA key. The RSA key is passed to the Encryptor
    class which does the encryption and decryption.
    Due to the size of the RSA key generated in RSAFile.py,
    the max character count to be encrypted cannot be
    greater than 240, so encryption is done line by line.
    """

    def __init__(self, filepath, rsa_filepath):
        super().__init__(str(filepath))
        self.rsa_filepath = str(rsa_filepath)
        self.encryptor = Encryptor(self.rsa_filepath)

    def encrypt(self, no_write=False):
        """
        Checks that the file is not encrypted and exists,
        then encrypts the contents through the Encryptor
        class and writes the bytes to the file.
        """
        if self.is_encryptable():
            file_lines = self.get_lines_and_clear_file(self.get_lines_as_list_from_text_file)

            for line in file_lines:
                line = self.clean_line(line)
                encrypted_data = self.encrypt_line(line)
                self.write_to_file_by_line(encrypted_data, self.write_bytes_to_file, line_separator)
            self.is_encrypted = True
        else:
            print(self.get_filepath() + " does not exist.")

    def decrypt(self, no_write=False):
        """
        Checks if the file is encrypted and exists,
        then utilizes the Encryptor class to decrypt
        the data and write the text to the file.
        """
        if self.is_decryptable():
            file_lines = self.get_lines_and_clear_file(self.get_lines_as_list_from_bytes_file)

            for line in file_lines:
                if len(line):   # if line != b'', decrypt line
                    decrypted_data = self.decrypt_line(line)
                    self.write_to_file_by_line(decrypted_data, self.append_text_to_file, '\n')
                else:
                    self.write_text_to_file(self.get_contents_of_file().strip())
            self.is_encrypted = False
        else:
            print(self.get_filepath() + " does not exist.")

    def write_bytes_to_file(self, data):
        """
        Writes data to the file as bytes.
        """
        if self.filepath_exists():
            with open(self.filepath, 'ab') as env_file:
                env_file.write(data)
                env_file.close()
        else:
            print(self.get_filepath() + " does not exist.")

    def get_bytes_from_file(self):
        """
        Returns the contents of the encrypted file
        as bytes.
        """
        data = None
        with open(self.filepath, 'rb') as my_file:
            data = my_file.read()
        return data

    def get_lines_as_list_from_bytes_file(self):
        return self.get_bytes_from_file().split(line_separator)

    def clean_line(self, line):
        """
        Strip the line of whitespace at the beginning and end.
        This is function is called before being encrypted.
        """
        return line.strip()

    def write_to_file_by_line(self, data, write_to_file_fn, line_separator):
        write_to_file_fn(data)
        write_to_file_fn(line_separator)

    def get_lines_and_clear_file(self, get_lines_fn):
        file_lines = get_lines_fn()
        self.clear_file()
        return file_lines

    def encrypt_line(self, line):
        return self.encryptor.encrypt_data(line)

    def decrypt_line(self, line):
        return self.encryptor.decrypt_data(line)