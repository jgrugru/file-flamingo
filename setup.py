
from distutils.core import setup
from setuptools import find_packages, setup
from pathlib import Path

HERE = Path(__file__).parent

# The text of the README file
README = (HERE / "README.md").read_text()

setup(
    name = 'fileflamingo',         # How you named your package folder (MyLib)
    packages = find_packages(exclude=("tests",)),
    version = '0.0.7',      # Start with a small number and increase it with every change you make
    license='MIT',        # Chose a license from here: https://help.github.com/articles/licensing-a-repository
    description = 'A suite of Python base classes that simplify interactions with files.',   # Give a short description about your library
    author = 'Jeff Gruenbaum',
    author_email = 'jeff.gruenbaum@gmail.com',
    long_description=README,
    long_description_content_type="text/markdown",
    url = 'https://github.com/jgrugru/file-flamingo', 
    keywords = ["file", 'file abstraction', 'file functions', 'fileclass', 'class file', 'mixin'],
    install_requires=[
        "pycryptodome==3.10.1",
    ],
    include_package_data=True,
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
    ],
)

# flake8: noqa