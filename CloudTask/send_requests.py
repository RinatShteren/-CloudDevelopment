import requests
import json
import time

api_url = "https://g9mqatt3bf.execute-api.us-east-1.amazonaws.com/Prod/hello"
api_key = "LexUiNIvJA37ZiEax2JvF6s5bBpmu47rBQ9uULk1"
num_requests = 10

headers = {
    "x-api-key": api_key,
    "Content-Type": "application/json"
}

for i in range(num_requests):
    payload = {
        "delay": 42,
        "user_id": "user-{}".format(i)
    }
    response = requests.get(api_url, params=payload, headers=headers)

    # הדפסת ה-URL המלא
    full_url = response.url
    print(f"Full URL: {full_url}")

    print(f"Request {i + 1}: Status Code {response.status_code}")

    if response.status_code == 200:
        print("Response data:", response.json())  # הצגת הנתונים שהתקבלו
    else:
        try:
            print("Response data:", response.json())  # ניסיון לפרש כ-JSON
        except ValueError:
            print("Response is not JSON")

    time.sleep(2)
