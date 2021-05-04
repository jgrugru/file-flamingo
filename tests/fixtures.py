from sys import path as syspath
from os import path, chdir
from pytest import fixture
from random import choice
from string import ascii_uppercase

PARENT_DIR = path.abspath(path.join(path.dirname(__file__), path.pardir))

syspath.append(PARENT_DIR)

from fileflamingo.BaseFile import BaseFile              # noqa: E402
from fileflamingo.RSAFile import RSAFile                # noqa: E402
from fileflamingo.EncryptionFile import EncryptionFile  # noqa: E402
from fileflamingo.TextFile import TextFile              # noqa: E402
from fileflamingo.Encryptor import Encryptor            # noqa: E402

CONTENTS_OF_TEXT_FILE = "USERNAME=JGRUGRU\nPASSWORD=12341515134$@#$^"

TEST_FILE_LIST = [
    "env_path/.env",
    "./env_path/env",
    ".env_path/env",
    "env_path/env/",
    ".env_path/env/",
    "././././env/",
    "././././env",
    "../env_path/.env",
    "../env_path1/.env/"]

TEST_FILE_LINE_LIST = [
    ['', 'asdfasd', '\n', 'asdfadsf\n'],
    ['', '\n\n\n\n\n\n', '\n', 'asdfadsf\n'],
]

ENCRYPT_CHAR_LIMIT = 245


"""
This file contains all the fixtures and functions
needed to automate and simplify the testing of the
different classes.
"""


def create_file(fileclass, filepath, *args, **kwargs):
    my_file = fileclass(filepath, *args, **kwargs)
    my_file.create_filepath()
    return my_file


def create_base_file(filepath, create_filepath=True):
    my_file = BaseFile(filepath)
    if create_filepath:
        my_file.create_filepath()
    return my_file


def str_factory(str_size):
    return ''.join(choice(ascii_uppercase) for i in range(str_size))


def encrypted_bytes_generator(encryptor, str_to_encrypt):
    return encryptor.encrypt_data(str_to_encrypt)


@fixture
def base_file(tmp_path):
    my_file = create_file(BaseFile, path.join(tmp_path, 'test.txt'))
    return my_file


@fixture
def text_file(tmp_path):
    my_file = create_file(
        TextFile,
        path.join(tmp_path, 'test.txt'),
        txt=CONTENTS_OF_TEXT_FILE)
    return my_file


@fixture
def rsa_file(tmp_path):
    my_rsa_file = create_file(RSAFile, path.join(tmp_path, 'my_key.pem'))
    my_rsa_file.gen_pem_file()
    return my_rsa_file


@fixture
def encryptor(rsa_file):
    return Encryptor(rsa_file)


@fixture
def encryption_file(text_file, rsa_file):
    my_encrypytion_file = create_file(
        EncryptionFile,
        text_file,
        rsa_file)
    return my_encrypytion_file


@fixture
def large_txt_file():
    return BaseFile(path.abspath(path.join(path.dirname(__file__),
                    'test_env.txt')))


@fixture
def env_setup_for_file_object(tmp_path):
    chdir(tmp_path)
