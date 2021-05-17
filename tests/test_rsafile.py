from os import path

from fileflamingo.RSAFile import RSAFile


def test_rsafile_gen_pem_file(tmp_path):
    filepath = path.join(tmp_path, "my_key.pem")
    my_file = RSAFile(filepath)
    my_file.gen_pem_file()
    assert my_file.is_file()
    assert path.exists(str(my_file))
