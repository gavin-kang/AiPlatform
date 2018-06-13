import requests

# endpoint = "http://localhost:5000/predict/lr"
endpoint = "http://192.168.50.32:5000/predict/lr"
json_data = {"features": [[20.3, 60.0, 1008.0, 85.0], [26, 70, 1152.0, 60.0]]}
result = requests.post(endpoint,json=json_data)
print(type(result))
print(result)
