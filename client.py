import requests

endpoint = "http://127.0.0.1:5000/test"
json_data = {"features": [[20.3, 60.0, 1008.0, 85.0, ], [26, 70, 1152.0, 60.0]],"steps":100}
result = requests.post(endpoint, ).json()
print(result)
