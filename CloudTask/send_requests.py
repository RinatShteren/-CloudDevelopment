import requests
import json
import time

api_url = "https://g9mqatt3bf.execute-api.us-east-1.amazonaws.com/Prod/hello"
num_requests = 10

for i in range(num_requests):
    payload = {
        "delay": 42,
        "user_id": "user-{}".format(i)
    }

    response = requests.get(api_url, params=payload)

    if response.status_code == 200:
        print(f"Request {i + 1}: Success")
    else:
        print(f"Request {i + 1}: Failed with status code {response.status_code}")

    time.sleep(0.5)  # 100ms delay between requests
