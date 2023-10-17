"""
Test API's by sending POST/GET requests

Supported APIs:

    - api/v1/exportJS
"""


import sys
import requests

base = "http://127.0.0.1:5000/"
path = "api/v1/"


def exportJS():
    name = "exportJS"

    headers = {
        "Content-Type": "application/json",
    }

    data = {
        "attributes": [
            {
                "name": "asfasf",
                "levels": [{"name": "1", "weight": 0.5}, {"name": "2", "weight": 0.5}],
            },
            {
                "name": "asf",
                "levels": [{"name": "3", "weight": 0.5}, {"name": "4", "weight": 0.5}],
            },
        ]
    }

    response = requests.post(base + path + name, headers=headers, json=data)

    print("Response status: ", response.status_code)
    print("Response text", response.text)


# Map function names to functions
FUNCTION_MAP = {
    "exportJS": exportJS,
}

if __name__ == "__main__":
    if len(sys.argv) <= 1:
        print(f"\nInclude the name of the function to call!\n")
    elif len(sys.argv) > 1 and sys.argv[1] in FUNCTION_MAP:
        FUNCTION_MAP[sys.argv[1]]()
    else:
        print(f"\nFunction {sys.argv[1]} not recognized!\n")
