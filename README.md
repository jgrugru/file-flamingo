![build status](https://travis-ci.com/jgrugru/file-flamingo.svg?branch=main)

# file-flamingo
A suite of base classes that simplifies interactions with files.

```
pip3 install fileflamingo
```

* Summary
* Base Classes
  * [BaseFile](https://github.com/jgrugru/file-flamingo#BaseFile)
  * [EncryptionFile](https://github.com/jgrugru/file-flamingo#EncryptionFile)

# BaseFile
```python
BaseFile(filepath)
```
Functions:
- get_contents_of_file (only works with text)
- create_filepath (either a file or a dir)
- delete_file (only works on files, not dirs)
- append_data_to_file
- write_data_to_file
- clear_file
- is_binary
- is_empty
- is_dir
- is_file
- filepath_exists

# EncryptionFile
```python
EncryptionFile(filepath, rsa_filepath)
```
Functions:
- encrypt
- decrypt
- write_bytes_to_file
- get_bytes_from_file

#### EncryptionFile Example:
```python
from fileflamingo.EncryptionFile import EncryptionFile

my_file = EncryptionFile("./encrypted.txt", './my_key.pem')

my_file.create_filepath()
my_file.append_data_to_file("I am about to be encrypted.")
my_file.encrypt()
```