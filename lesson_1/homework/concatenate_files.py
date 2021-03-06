from functools import partial
from hashlib import md5
import os


def divide_file(path, size_of_piece, result_name):
    with open(result_name, "w") as all_hashes_handle:
        with open(path, "rb") as file_handle:
            read_block = partial(file_handle.read, size_of_piece)
            # Read until it reaches the end
            for piece_number, block in enumerate(iter(read_block, b"")):
                with open(str(piece_number), "wb") as write_handle:
                    write_handle.write(block)
                    current_hash = count_hash(block)
                    all_hashes_handle.write(current_hash)
            return piece_number


def count_hash(data):
    h = md5()
    h.update(data)
    return h.hexdigest()


def concat_files(directory, result_name):
    hash_to_file = {}
    files_list = os.listdir(directory)
    for file in files_list:
        full_path = os.path.join(directory, file)
        if file.endswith(".md5"):
            all_hashes_handle = open(full_path)
            ordered_hashes = map(lambda x: x.rstrip("\n"), all_hashes_handle)
        else:
            with open(full_path, "rb") as file_handle:
                hash_sum = count_hash(file_handle.read())
                hash_to_file[hash_sum] = full_path

    with open(result_name, "wb") as write_handle:
        for current_hash in ordered_hashes:
            current_file_path = hash_to_file[current_hash]
            with open(current_file_path, "rb") as read_handle:
                write_handle.write(read_handle.read())
