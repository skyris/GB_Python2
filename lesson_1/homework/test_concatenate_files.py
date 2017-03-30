import filecmp
import os
from concatenate_files import concat_files


def test():
    directory = "/home/victor/projects/GB_Python2/GB_Python2/lesson_1/homework/files/file1"
    result_path = os.path.join(directory, "result")
    concat_files(directory, result_path)
    assert filecmp.cmp(os.path.join(directory, "Sly_Pablo.jpg"), result_path), "Files don't match"
    os.remove(result_path)
