from Crypto.PublicKey import RSA

from .BaseFile import BaseFile


class RSAFile(BaseFile):
    """
    Inherits all the functions from BaseFile.
    An abstraction of an RSA file saved as a
    pem file. Allows the user to generate the
    key in a pem file and grab the key for
    use in encryption.
    """

    def __init__(self, filepath):
        super().__init__(str(filepath))

    def gen_key(self, size=2048):
        """
        Generates the RSA key.
        """
        return RSA.generate(size)

    def gen_pem_file(self):
        """
        Calls the gen_key function and stores the
        key into a pem file.
        """
        key = self.gen_key()
        f = open(self.filepath, 'wb')
        f.write(key.export_key('PEM'))
        f.close()

    def get_key(self):
        """
        Returns the RSA key from the file.
        """
        key = None

        if self.filepath_exists():
            with open(self.filepath, 'r') as pem_file:
                key = RSA.import_key(pem_file.read())
        else:
            print(self.filepath + " does not exist.")

        return key
