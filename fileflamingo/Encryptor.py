from Crypto.Cipher import PKCS1_v1_5 as Cipher_PKCS1_v1_5
from Crypto.PublicKey import RSA


class Encryptor():
    """
    This class utilizes the Crypto PyPi package.
    Accepts an RSA key as an argument. The
    encrypt and decrypt class use the key
    with the Cipher_PKCS1_v1_5 algorithm.
    """

    def __init__(self, rsa_filepath):
        self.pem_key = self.get_key(str(rsa_filepath))

    def encrypt_data(self, data):
        cipher = Cipher_PKCS1_v1_5.new(self.pem_key)
        if cipher.can_encrypt():
            return cipher.encrypt(data.encode())
        else:
            print("ERROR: cannot encrypt with pem.")

    def decrypt_data(self, data):
        decipher = Cipher_PKCS1_v1_5.new(self.pem_key)
        return decipher.decrypt(data, None).decode()

    def get_key(self, rsa_filepath):
        with open(rsa_filepath, 'r') as pem_file:
            key = RSA.import_key(pem_file.read())
        return key
