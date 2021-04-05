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
- encrypt
- decrypt
- write_bytes_to_file
- get_bytes_from_file