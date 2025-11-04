import requests

# Change this to your VM public IP later, for now use localhost
URL = "http://localhost:5002/api/execute"

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

