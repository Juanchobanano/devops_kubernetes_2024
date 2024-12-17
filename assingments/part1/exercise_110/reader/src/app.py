# reader.py
import time
import hashlib
import os

directory = os.path.join('/', 'usr', 'src', 'app', 'files')
file_path = f"{directory}/log.txt"


def compute_hash(line):
    return hashlib.sha256(line.encode()).hexdigest()


while True:
    try:
        with open(file_path, "r") as file:
            lines = file.readlines()
            for line in lines:
                line = line.strip()
                if line:
                    print(f"{line} -> {compute_hash(line)}")
    except FileNotFoundError:
        print("Waiting for the file...")
    time.sleep(5)
