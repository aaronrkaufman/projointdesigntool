"""
Test API's by sending POST/GET requests

Supported APIs:

    - api/v1/exportJS
"""


import requests

base = "http://127.0.0.1:5000/"
path = "api/v1/exportJS"

headers = {
    "Content-Type": "application/json",
}

data = {
    "attributes": [
        "asfasf",
        "asf",
    ],
    "level_dict": {
        "asfasf": ["1", "2"],
        "asf": ["3", "4"],
    },
}

response = requests.post(base + path, headers=headers, json=data)

print(response)
