from .TextFile import TextFile
from .ByteFile import ByteFile
from .Encryptor import Encryptor


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
            self.map_file_lines(encrypted_file_lines, self.append_byte_line_to_file)
            self.is_encrypted = True
        else:
            print(
                self.get_filepath()
                + " does not exist or is \
                  not encryptable."
            )

    def decrypt(self):
        """
        Checks if the file is decryptable,
        then utilizes the Encryptor class to decrypt
        the data and write the text to the file.
        """
        if self.is_decryptable():
            decrypted_file_lines = self.decrypt_byte_lines()
            self.clear_file()
            self.map_file_lines(decrypted_file_lines, self.append_text_line_to_file)
            self.write_text_to_file(self.get_contents_of_file().strip())
            self.is_encrypted = False
        else:
            print(
                self.get_filepath()
                + " does not exist or is \
                  not encryptable."
            )

    def encrypt_text_lines(self):
        """
        Grabs the file lines from the text file as a list.
        Then encrypts each line in the list and returns
        the encrypted file lines in a new list.
        """
        file_lines = self.get_text_lines_as_list()
        encrypted_file_lines = self.map_file_lines(file_lines, self.encrypt_line)
        return encrypted_file_lines

    def decrypt_byte_lines(self):
        """
        Grabs the byte lines from the byte file as a list.
        Then decrypts each line in the list and returns
        the decrypted file lines in a new list.
        """
        file_lines = self.get_byte_lines_as_list()
        decrypted_file_lines = self.map_file_lines(file_lines, self.decrypt_line)
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
        If line == b'', the function returns None.
        This is accomplished through the boolean
        expression len(line) == 0.
        """
        if len(line):
            return self.encryptor.decrypt_data(line)
        else:
            return None
