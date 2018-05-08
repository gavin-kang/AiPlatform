import requests

def main():
  endpoint = "http://127.0.0.1:8500"
  json_data = {"model_name": "default", "data": {"keys": [[1], [8]], "features": [[1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0], [2.0, 2.0, 2.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0]]} }
  result = requests.post(endpoint, json=json_data)
  print(result.text)

if __name__ == "__main__":
  main()