from .TextFile import TextFile
from .ByteFile import ByteFile
from .Encryptor import Encryptor
from .FileLines import map_file_lines


class EncryptionFile(TextFile, ByteFile):
    """
    EncryptionFile class inherits from TextFile and ByteFile.
    EncryptionFile allows you to encrypt and decrypt the contents
    of the file. Constructor requires a filepath to an RSA key.
    The RSA key is passed to the Encryptor class which does the
    encryption and decryption. Due to the size of the RSA key
    generated in RSAFile.py, the max character count to be
    encrypted cannot be greater than 240, so encryption is
    done line by line.
    """

    def __init__(self, filepath, rsa_filepath):
        super().__init__(str(filepath))
        self.rsa_filepath = str(rsa_filepath)
        self.encryptor = Encryptor(self.rsa_filepath)

    def encrypt(self):
        """
        Checks that the file is_encryptable,
        then encrypts the contents through the Encryptor
        class and writes the bytes to the file.
        """
        if self.is_encryptable():
            encrypted_file_lines = self.encrypt_text_lines()
            self.clear_file()
            map_file_lines(encrypted_file_lines,
                                self.write_byte_line_to_file)
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
            decrypted_file_lines = self.decrypt_byte_lines()
            self.clear_file()
            map_file_lines(decrypted_file_lines,
                                self.append_text_line_to_file)
            self.write_text_to_file(self.get_contents_of_file().strip())
            self.is_encrypted = False
        else:
            print(self.get_filepath() + " does not exist.")

    def encrypt_text_lines(self):
        """
        Grabs the lines from the text file as a list and
        then encrypts each item in the list and returns
        the encrypted items in a new list.
        """
        file_lines = self.get_text_lines_as_list()
        encrypted_file_lines = map_file_lines(file_lines,
                                              self.encrypt_line)
        return encrypted_file_lines

    def decrypt_byte_lines(self):
        """
        Grabs the lines from the binary file as a list and
        then decrypts each item in the list and returns
        the decrypted items in a new list.
        """
        file_lines = self.get_lines_as_list_from_byte_file()
        decrypted_file_lines = map_file_lines(file_lines,
                                              self.decrypt_line)
        decrypted_file_lines.remove(None)
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
