[![build status](https://travis-ci.com/jgrugru/file-flamingo.svg?branch=main)](https://travis-ci.com/jgrugru/file-flamingo)

# file-flamingo
A suite of base classes that simplifies interactions with files.

```
pip3 install fileflamingo
```

* :books: Base Classes
  * [BaseFile](https://github.com/jgrugru/file-flamingo#BaseFile)
  * [EncryptionFile](https://github.com/jgrugru/file-flamingo#EncryptionFile)
  * [RSAFile](https://github.com/jgrugru/file-flamingo#RSAFile)

```python
from fileflamingo.BaseFile import BaseFile
from fileflamingo.RSAFile import RSAFile
from fileflamingo.EncryptionFile import EncryptionFile

base_file = BaseFile("./my_text.txt")
base_file.create_filepath()
base_file.append_data_to_file("I am about to be encrypted.")

rsa_file = RSAFile('./my_key.pem')
rsa_file.gen_pem_file() # Creates an rsa key and writes it to my_key.pem.

encryption_file = EncryptionFile(base_file.get_filepath(), rsa_file.get_filepath())

encryption_file.encrypt() # Encrypt ./my_text.txt with the encrypt function.
print(my_file.get_bytes_from_file())

encryption_file.decrypt() # It can be decrypted with the decrypt() function.
print(my_file.get_contents_of_file())
```
Output:
```
b'\x8cZc\x1bA*\xbb\x00\xc5\x1a\x0e)\x8d\x1f\x05+\xa0\x81\xda\xb9\x91\n\n\x17J p\xb0\x0f>\xf3)\xf9*\xda\x97J\x1b\x94\x11Q\xe7\xdd\x84\x1c\x1ca9)\xdcY\x0e\x95\x11\xbf=\xfb8\x88\x88f\xc1\xf2\xfeV\\\x8d\\~]\xef\t\xac\x8b\xa0+\xf5W\xf5\xea\x04\tU\xe2[\xd6v\xad\x08Z\xd7\x82\x08\x07\xd2\x8bS\xc4\xbe\xc2e\x96\x7fk\xe8\xb5S\xa4\x95;\x12Y\x83\x11\xbe\xa6\x82!\xf4\x18\xef\xf1\xce\xdd\x934Ay\x08\xd9\xfa\t.\x00b\xdfvY( \x8a\xed\xdc\xd8\xeb\x12\xf2\xf0\xa6G\x08T#\x91p\xb2<\xe6\xf9\x94)J\xe2le\x13\x02\x92s\xbb\xbd\xc8\xebI\xb4\x041\xa0\x9d\xbfy?\xe3\xe4\xa7\x98\x07pX\x87\xda\xd9\xba\xd5c3\rWBv0\x17\xf7\xff}\x1d\x83\xf5\xc6)\xdd||\xe8\xd0\x90^$\xae\xbb\xf7Kc\x15.\xd8\xa8F\x16\xee\xb5\x00z<\xd88\x05Z,\xef\xc0\xe1\xbe\xfdY\xb0\xa5\x1aX\xa3R"o\xf2\x9c\xbe'
I am about to be encrypted.
```

# BaseFile
```python
BaseFile(filepath)
```
Functions:
- create_filepath (either a file or a dir)
- delete_file (only works on files, not dirs)
- clear_file
- get_contents_of_file (only works with text)
- append_text_to_file
- write_text_to_file
- is_binary
- is_empty
- is_dir
- is_file
  is_decryptable
  is_encryptable
- filepath_exists

# TextFile
```python
TextFile(filepath, txt="This is added to the file.")
```
The TextFile does not add functionality but allows the user
to create text files with content at initialization.
The _txt_ is appended to the file, so if the file already
exists, the text is appended.

# EncryptionFile
```python
EncryptionFile(filepath, rsa_filepath)
```
Functions:
- encrypt
- decrypt
- write_bytes_to_file
- get_bytes_from_file

# RSAFile
```python
RSAFile(filepath)
```
Functions:
- gen_key
- gen_pem_file
- get_key
