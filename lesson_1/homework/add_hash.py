import hashlib
import csv
import tempfile


def add_hash(file_name):
    with tempfile.TemporaryFile(mode="w+t") as temp_file:
        with open(file_name, "r+", newline='') as file_reader:
            csv_reader = csv.reader(file_reader, delimiter=";")
            csv_writer = csv.writer(temp_file, delimiter=";")
            for row in csv_reader:
                byte_string = row[0].encode()
                algorithm_name = row[1]
                m = hashlib.new(algorithm_name)
                m.update(byte_string)
                hash_sum = m.hexdigest()
                row[2] = hash_sum
                csv_writer.writerow(row)
            temp_file.seek(0)
            file_reader.seek(0)
            for line in temp_file.read():
                file_reader.write(line)


if __name__ == "__main__":
    add_hash("need_hashes.csv")
