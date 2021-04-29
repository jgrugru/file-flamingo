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

    def encrypt(self):
        """
        Checks that the file is not encrypted and exists,
        then encrypts the contents through the Encryptor
        class and writes the bytes to the file.
        """
        if self.is_encryptable():
            encrypted_file_lines = self.get_encrypted_lines_as_list()
            self.clear_file()
            self.write_file_lines_to_file(encrypted_file_lines,
                                          self.append_bytes_to_file,
                                          line_separator)
            self.is_encrypted = True
        else:
            print(self.get_filepath() + " does not exist.")

    def decrypt(self):
        """
        Checks if the file is encrypted and exists,
        then utilizes the Encryptor class to decrypt
        the data and write the text to the file.
        """
        if self.is_decryptable():
            decrypted_file_lines = self.get_decrypted_lines_as_list()
            self.clear_file()
            self.write_file_lines_to_file(decrypted_file_lines,
                                          self.append_text_to_file,
                                          '\n')
            self.write_text_to_file(self.get_contents_of_file().strip())
            self.is_encrypted = False
        else:
            print(self.get_filepath() + " does not exist.")

    def get_encrypted_lines_as_list(self):
        """
        Grabs the lines from the text file as a list and
        then encrypts each item in the list and returns
        the encrypted items in a new list.
        """
        file_lines = self.get_lines_as_list_from_text_file()
        encrypted_file_lines = self.encrypt_decrypt_file_lines(
                file_lines, self.encrypt_line)
        return encrypted_file_lines

    def get_decrypted_lines_as_list(self):
        """
        Grabs the lines from the binary file as a list and
        then decrypts each item in the list and returns
        the decrypted items in a new list.
        """
        file_lines = self.get_lines_as_list_from_bytes_file()
        decrypted_file_lines = self.encrypt_decrypt_file_lines(
                    file_lines, self.decrypt_line)
        return decrypted_file_lines

    def encrypt_line(self, line):
        """
        Before returning the encrypted line, the line
        is stripped to remove any whitespace.
        """
        clean_line = line.strip()
        return self.encryptor.encrypt_data(clean_line)

    def decrypt_line(self, line):
        """
        Returns the decrypted line if the line != b''.
        If line == b'' / len(line) == 0, returns None.
        """
        if len(line):
            return self.encryptor.decrypt_data(line)
        else:
            return None

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

    def append_bytes_to_file(self, data):
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
        """
        Returns a list of bytes in the file
        split at the line_separator.
        """
        return self.get_bytes_from_file().split(line_separator)

    def encrypt_decrypt_file_lines(self, file_lines, encrypt_or_decrypt_fn):
        """
        Accepts a file_lines list and creates a new list with
        the contents either encrypted or decrypted. 
        encrypt_or_decrypt_fn accepts functions encrypt_line
        and decrypt_line.
        """
        lines_list = []
        for line in file_lines:
            new_line = encrypt_or_decrypt_fn(line)
            lines_list.append(new_line)
        return lines_list

    def write_file_lines_to_file(self,
                                 file_lines,
                                 write_to_file_fn,
                                 line_separator):
        """
        Accepts file_lines list either encrypted or decrypted. Loops
        through the list and writes a line to the file followed by
        the line_separator. Acceptable functions passed in are
        append_bytes_to_file and append_text_to_file.

        """
        for line in file_lines:
            write_to_file_fn(line)
            write_to_file_fn(line_separator)
