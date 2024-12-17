# writer.py
import time
from datetime import datetime
import os

directory = os.path.join('/', 'usr', 'src', 'app', 'files')
file_path = f"{directory}/log.txt"

while True:
    with open(file_path, "a") as file:
        timestamp = datetime.utcnow().isoformat()
        file.write(f"{timestamp}\n")
    time.sleep(5)
