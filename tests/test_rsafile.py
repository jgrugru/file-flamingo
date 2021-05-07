from sys import path as syspath
from os import path

PARENT_DIR = path.abspath(path.join(path.dirname(__file__), path.pardir))

syspath.append(PARENT_DIR)

from fileflamingo.RSAFile import RSAFile  # noqa: E402


def test_rsafile_gen_pem_file(tmp_path):
    filepath = path.join(tmp_path, "my_key.pem")
    my_file = RSAFile(filepath)
    my_file.gen_pem_file()
    assert my_file.is_file()
    assert path.exists(str(my_file))
