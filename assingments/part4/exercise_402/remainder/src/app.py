import requests
import constants as ct

data = requests.get(ct.WIKIPEDIA_URL)
json_data = {"description": data.url}
response = requests.post(
    ct.TODOS_ENDPOINT,
    json=json_data)
print(response.status_code)
print(response.json())
