from os import path
from pytest import mark, fail

from fileflamingo.EncryptionFile import EncryptionFile
from fileflamingo.TextFile import TextFile
from tests.fixtures import (
    rsa_file,  # noqa: F401
    encryptor,
    encryption_file,
    text_file,
    base_file,
)
from tests.fixtures import str_factory, create_file, encrypted_bytes_generator
from tests.fixtures import ENCRYPT_CHAR_LIMIT


PARENT_DIR = path.abspath(path.join(path.dirname(__file__), path.pardir))


@mark.parametrize(
    "str_to_encrypt, exception_raised",
    [
        (str_factory(ENCRYPT_CHAR_LIMIT), False),  # why is this the limit?
        ("USERNAME=" + str_factory(236), False),
        ("PASSWORD=" + "aJh@WDFWDg-#4jZr" + str_factory(100), False),
        ("TESTING=" + "aJh@WDFWDg-#4jZr" + str_factory(250), True),
    ],
)
def test_encryptor_encrypt_and_decrypt_data(
    encryptor, str_to_encrypt, exception_raised  # noqa: F811
):
    was_exception_raised = False
    try:
        data = encryptor.encrypt_data(str_to_encrypt)
    except ValueError:
        was_exception_raised = True
    if not was_exception_raised:
        assert isinstance(data, bytes)
    assert was_exception_raised == exception_raised


@mark.parametrize(
    "original_str, is_decryptable",
    [
        (str_factory(ENCRYPT_CHAR_LIMIT), False),
        (str_factory(ENCRYPT_CHAR_LIMIT), True),
        (str_factory(140), True),
        (str_factory(1), True),
        ("0", True),
        ("aJh@WDFWDg-#4jZr", True),
    ],
)
def test_encryptor_decrypt_and_decrypt_data(
    encryptor, original_str, is_decryptable  # noqa: F811
):
    if is_decryptable:
        str_to_decrypt = encrypted_bytes_generator(encryptor, original_str)
    else:
        str_to_decrypt = str.encode(original_str)
    was_exception_raised = False
    try:
        data = encryptor.decrypt_data(str_to_decrypt)
    except ValueError:
        was_exception_raised = True
    if not was_exception_raised:
        assert data == original_str
    assert was_exception_raised != is_decryptable


@mark.parametrize(
    "str_to_encrypt, expected_output",
    [
        (
            str_factory(ENCRYPT_CHAR_LIMIT)
            + "\n"
            + str_factory(ENCRYPT_CHAR_LIMIT)
            + "\n"
            + str_factory(ENCRYPT_CHAR_LIMIT),
            None,
        ),
        (str_factory(140), None),
        ("\n\n\n\n\n\n\n\n", ""),
        ("\t\t\t\t\t\t\n\n\n", ""),
        (" test=12345 \n test1=12345 \n", "test=12345\ntest1=12345"),
        (str_factory(1), None),
        ("0", None),
        ("", None),
        (
            str_factory(100)
            + "aJh@WDFWDg-#4jZr"
            + str_factory(10)
            + "\n"
            + str_factory(ENCRYPT_CHAR_LIMIT)
            + "\n"
            + str_factory(ENCRYPT_CHAR_LIMIT),
            None,
        ),
        (
            open(
                path.abspath(path.join(PARENT_DIR, "tests/etc/test_env.txt")), "r"
            ).read(),
            None,
        ),
    ],
)
def test_encryptionfile_encrypt_decrypt_file(
    tmp_path, rsa_file, str_to_encrypt, expected_output  # noqa: F811
):
    txt_file = create_file(
        TextFile, path.join(tmp_path, "test.txt"), txt=str_to_encrypt
    )
    encryption_file = create_file(EncryptionFile, txt_file, rsa_file)  # noqa: F811
    encryption_file.encrypt()
    assert encryption_file.is_binary()
    encryption_file.decrypt()
    contents_after_encryption = encryption_file.get_contents_of_file()
    assert not encryption_file.is_binary()
    if isinstance(expected_output, str):
        assert expected_output == contents_after_encryption
    else:
        assert str_to_encrypt == contents_after_encryption


@mark.parametrize(
    "random_bytes, exception_raised",
    [
        (str_factory(ENCRYPT_CHAR_LIMIT), True),
        (str.encode(str_factory(140)), False),
        (str.encode(str_factory(ENCRYPT_CHAR_LIMIT * 3)), False),
        (b"aJh@WDFWDg-#4jZr", False),
    ],
)
def test_encryptionfile_write_and_get_bytes(
    encryption_file, random_bytes, exception_raised  # noqa: F811
):
    encryption_file.clear_file()
    was_exception_raised = False
    try:
        encryption_file.write_bytes_to_file(random_bytes)
    except TypeError:
        was_exception_raised = True

    if not was_exception_raised:
        assert random_bytes == encryption_file.get_bytes_from_file()

    assert was_exception_raised == exception_raised


def test_encryptionfile_accepts_file_object_as_arguments(
    base_file, rsa_file
):  # noqa: E501, F811
    try:
        EncryptionFile(base_file, rsa_file)
    except TypeError:
        fail(
            "Failed -- TypeError -- on \
             test_encryptionfile_accepts_file_object_as_arguments."
        )
