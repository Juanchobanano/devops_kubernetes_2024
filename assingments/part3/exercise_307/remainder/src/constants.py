import os

WIKIPEDIA_URL = "https://en.wikipedia.org/wiki/Special:Random"
TODOS_HOST = os.environ.get("TODOS_HOST", "localhost")
TODOS_PORT = int(os.environ.get("TODOS_PORT", 9030))
TODOS_ENDPOINT = f"http://{TODOS_HOST}:{TODOS_PORT}/todos"
