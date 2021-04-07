from .BaseFile import BaseFile
from .Encryptor import Encryptor


class EncryptionFile(BaseFile):
    """
    EncryptionFile class inherits from BaseFile. EncryptionFile allows you to
    encrypt and decrypt the contents of the file. Constructor requires a
    filepath to an RSA key. The RSA key is passed to the Encryptor
    class which does the encryption and decryption.
    """

    def __init__(self, filepath, rsa_filepath):
        self.filepath = filepath
        self.rsa_filepath = rsa_filepath
        self.encryptor = Encryptor(str(rsa_filepath))
        self.is_encrypted = self.is_binary()

    def decrypt(self):
        """
        Checks if the file is encrypted and exists,
        then utilizes the Encryptor class to decrypt
        the data and write the text to the file.
        """
        if self.filepath_exists() and self.is_encrypted:
            decrypted_data = self.encryptor.decrypt_data(
                self.get_bytes_from_file())
            self.write_data_to_file(decrypted_data)
            self.is_encrypted = False
        else:
            print(self.get_filepath() + " does not exist.")

    def encrypt(self):
        """
        Checks that the file is not encrypted and exists,
        then encrypts the contents through the Encryptor
        class and writes the bytes to the file.
        """
        if self.filepath_exists() and not self.is_encrypted:
            encrypted_data = self.encryptor.encrypt_data(
                self.get_contents_of_file())
            self.write_bytes_to_file(encrypted_data)
            self.is_encrypted = True
        else:
            print(self.get_filepath() + " does not exist.")

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

    def get_bytes_from_file(self):
        """
        Returns the contents of the encrypted file
        as bytes.
        """
        data = None
        with open(self.filepath, 'rb') as my_file:
            data = my_file.read()
        return data
