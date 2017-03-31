import os
import pytest
from pep8_me import create_file


@pytest.mark.parametrize("file_name, directory, size, result_bytes_size", [
    ("test1.txt", "/home/victor/", "2KB", 2048),
    ("test2.txt", "/home/victor/", "10KB", 10240),
    ("test3.txt", "/home/victor/", "1024", 1024),
    ("test4.txt", "/home/victor/", "2MB", 2097152),
    ("test5.txt", "/home/victor/", "1B", 1)
])
def test_size_of_file(file_name, directory, size, result_bytes_size):
    file_path = os.path.join(directory, file_name)
    create_file(file_name, directory, size)
    assert os.path.getsize(file_path) == result_bytes_size, "Wrong file size"
    os.remove(file_path)
