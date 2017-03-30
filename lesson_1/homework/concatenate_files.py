from functools import partial


def divide_file(path, size_of_piece):
    with open(path, "rb") as file_handle:
        read_block = partial(file_handle.read, size_of_piece)
        # Read until it reaches the end
        for piece_number, block in enumerate(iter(read_block, b"")):
            with open(str(piece_number), "wb") as write_handle:
                write_handle.write(block)
        return piece_number


if __name__ == "__main__":
    print(divide_file("need_hashes.csv", 50))
