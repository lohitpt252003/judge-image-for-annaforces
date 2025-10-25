import requests

# Change this to your VM public IP later, for now use localhost
URL = "http://80.225.200.111:5000/api/execute"

payload = {
    "code": "print('Hello from inside container!')",
    "language": "python",
    "stdin": "",
    "timelimit": 2,
    "memorylimit": 256
}

try:
    response = requests.post(URL, json=payload)
    print("Status Code:", response.status_code)
    print("Response JSON:", response.json())
except Exception as e:
    print("Error:", e)

