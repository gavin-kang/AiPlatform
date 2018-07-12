# USAGE
# python simple_request.py

# import the necessary packages
import requests

# initialize the Keras REST API endpoint URL along with the input
# image path
KERAS_REST_API_URL = "http://localhost:5000/train/lr"
IMAGE_PATH = "timg.jpg"

# load the input image and construct the payload for the request
#image = open(IMAGE_PATH, "rb").read()
#payload = {"image": image}


payload = {"filepath": "F:\AIPlatform\AiPlatform\data\data.xls","y_lable":"PE","train_type":"lr"}
res=requests.post(KERAS_REST_API_URL,payload).json()
print(res)


