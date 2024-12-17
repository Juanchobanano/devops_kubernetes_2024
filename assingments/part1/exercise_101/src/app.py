import time
import random
import string
from datetime import datetime


def generate_random_string(length=8):
    """Generate a random string of given length."""
    return ''.join(random.choices(
        string.ascii_letters + string.digits, k=length))


def main():
    # Generate a random string and store it in memory
    random_string = generate_random_string()
    print(f"Generated random string: {random_string}\n")

    # Continuously output the string with a timestamp every 5 seconds
    while True:
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        print(f"[{timestamp}] {random_string}")
        time.sleep(5)


if __name__ == "__main__":
    main()
