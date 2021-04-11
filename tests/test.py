import sys
from os import path, chdir
from pytest import fixture, mark

sys.path.append(path.abspath(path.join(path.dirname(__file__),
                path.pardir)))

from fileflamingo.BaseFile import BaseFile              # noqa: E402
from fileflamingo.RSAFile import RSAFile                # noqa: E402
from fileflamingo.EncryptionFile import EncryptionFile  # noqa: E402


@fixture
def base_file(tmp_path):
    my_file = BaseFile(path.join(tmp_path, 'env', '.env'))
    my_file.create_filepath()
    return my_file


@fixture
def base_file_with_content(base_file):
    base_file.append_data_to_file("0123456789")
    return base_file


@fixture
def env_setup_for_file_object(tmp_path):
    chdir(tmp_path)


@fixture
def rsa_file(tmp_path):
    my_rsa_file = RSAFile(path.join(tmp_path, 'my_key.pem'))
    my_rsa_file.gen_pem_file()
    return my_rsa_file


@fixture
def encryption_file(base_file_with_content, rsa_file):
    my_encrpytion_file = EncryptionFile(
        base_file_with_content.get_filepath(),
        rsa_file.get_filepath())
    return my_encrpytion_file


@mark.parametrize("file_path, expected_result, is_file", [
    ("env_path/.env", True, True),
    ("./env_path/env", True, True),
    (".env_path/env", True, True),
    ("env_path/env/", True, False),
    (".env_path/env/", True, False),
    ("././././env/", True, False),
    ("././././env", True, True),
    ("../env_path/.env", True, True),
    ("../env_path1/.env/", True, False),
])
def test_basefile_create_and_delete_filepath(env_setup_for_file_object,
                                             file_path,
                                             expected_result,
                                             is_file):
    my_file = BaseFile(file_path)
    my_file.create_filepath()
    assert my_file.filepath_exists() == expected_result
    assert path.isfile(my_file.get_filepath()) == is_file
    my_file.delete_file()
    assert my_file.filepath_exists() != is_file


def test_basefile_get_contents_of_text_file(base_file_with_content):
    assert base_file_with_content.get_contents_of_file() == '0123456789'


def test_basefile_clear_file(base_file, base_file_with_content):
    base_file_with_content.clear_file()
    assert base_file_with_content.is_empty()
    base_file.clear_file()
    assert base_file.is_empty()


def test_basefile_str(base_file):
    assert base_file.get_filepath() == str(base_file)


def test_encryptionfile_encrypt_and_decrypt(encryption_file):
    encryption_file.encrypt()
    assert encryption_file.is_binary()
    encryption_file.decrypt()
    assert not encryption_file.is_binary()


def test_rsafile_gen_pem_file(rsa_file):
    assert rsa_file.filepath_exists()


def test_rsafile_get_key(rsa_file):
    assert rsa_file.get_key()
