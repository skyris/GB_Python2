import os
import random
import re
import string


def create_file(file_name, directory, size):
    regex = r"(\d+)([a-zA-Z]*)"
    value, suffix = re.findall(regex, size)[0]
    suffix_to_bytes = {
        "": 1,
        "B": 1,
        "KB": 1024,
        "MB": 1048576,
        "GB": 1073741824,
        "TB": 1099511627776
    }
    size_in_bytes = int(value) * suffix_to_bytes[suffix.upper()]
    alphanumeric_characters = string.ascii_letters + string.digits
    token = "".join(
        random.choice(alphanumeric_characters) for _ in range(size_in_bytes)
    )
    file_path = os.path.join(directory, file_name)
    file_handle = open(file_path, "w")
    file_handle.write(token)


if __name__ == "__main__":
    create_file("test1.txt", "/home/victor/", "2KB")
    create_file("test2.txt", "/home/victor/", "10KB")
    create_file("test3.txt", "/home/victor/", "1024")
    create_file("test4.txt", "/home/victor/", "2MB")
    create_file("test5.txt", "/home/victor/", "1B")
