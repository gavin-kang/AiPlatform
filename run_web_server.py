# import the necessary packages
from keras.preprocessing.image import img_to_array
from keras.applications import imagenet_utils
from PIL import Image
import numpy as np
import settings
import helpers
import flask
import redis
import uuid
import time
import json
import io
import pandas as pd
import run_model_tarining
from flask_cors import CORS

# initialize our Flask application and Redis server
app = flask.Flask(__name__)
CORS(app, supports_credentials=True)
db = redis.StrictRedis(host=settings.REDIS_HOST,
                       port=settings.REDIS_PORT, db=settings.REDIS_DB)


class MyEncoder(json.JSONEncoder):
    """json转换出问题的解决办法"""

    def default(self, obj):
        if isinstance(obj, np.integer):
            return int(obj)
        elif isinstance(obj, np.floating):
            return float(obj)
        elif isinstance(obj, np.ndarray):
            return obj.tolist()
        else:
            return super(MyEncoder, self).default(obj)


def prepare_image(image, target):
    # if the image mode is not RGB, convert it
    if image.mode != "RGB":
        image = image.convert("RGB")

    # resize the input image and preprocess it
    image = image.resize(target)
    image = img_to_array(image)
    image = np.expand_dims(image, axis=0)
    image = imagenet_utils.preprocess_input(image)

    # return the processed image
    return image


@app.route("/")
def homepage():
    return "Welcome to the PyImageSearch Keras REST API!"


@app.route("/predict/resNet50", methods=["POST"])
def predict():
    # initialize the data dictionary that will be returned from the
    # view
    data = {"success": False}

    # ensure an image was properly uploaded to our endpoint
    if flask.request.method == "POST":
        if flask.request.files.get("image"):
            # read the image in PIL format and prepare it for
            # classification
            image = flask.request.files["image"].read()
            image = Image.open(io.BytesIO(image))
            image = prepare_image(image,
                                  (settings.IMAGE_WIDTH, settings.IMAGE_HEIGHT))

            # ensure our NumPy array is C-contiguous as well,
            # otherwise we won't be able to serialize it
            image = image.copy(order="C")

            # generate an ID for the classification then add the
            # classification ID + image to the queue
            k = str(uuid.uuid4())
            image = helpers.base64_encode_image(image)
            d = {"id": k, "image": image}
            db.rpush(settings.IMAGE_QUEUE, json.dumps(d))

            # keep looping until our model server returns the output
            # predictions
            while True:
                # attempt to grab the output predictions
                output = db.get(k)

                # check to see if our model has classified the input
                # image
                if output is not None:
                    # add the output predictions to our data
                    # dictionary so we can return it to the client
                    output = output.decode("utf-8")
                    data["predictions"] = json.loads(output)

                    # delete the result from the database and break
                    # from the polling loop
                    db.delete(k)
                    break

                # sleep for a small amount to give the model a chance
                # to classify the input image
                time.sleep(settings.CLIENT_SLEEP)

            # indicate that the request was a success
            data["success"] = True

    # return the data dictionary as a JSON response
    return flask.jsonify(data)


@app.route("/train/lr", methods=["POST"])
def LinearRegression():
    data = {"success": False}
    if flask.request.method == "POST":
        if flask.request.files.get("excel"):
            exc = flask.request.files["excel"]
            df = pd.read_excel(exc)
            # res = run_model_tarining.train(df)
            data["success"] = True
        else:
            file_path = flask.request.form['filepath']
            y_lable = flask.request.form['y_lable']
            train_type = flask.request.form['train_type']
            if file_path != '':
                res = run_model_tarining.train(file_path=file_path, y_lable=y_lable, train_tpye=train_type)
            else:
                res = run_model_tarining.train(y_lable=y_lable, train_tpye=train_type)
            data["predictions"] = json.dumps(res, cls=MyEncoder)
            data["success"] = True
    return flask.jsonify(data)


@app.route("/predict/lr", methods=["POST"])
def predict_lr():
    result_data = {"success": False}
    # json_data = flask.request.form["features"]
    json_data = flask.request.get_json("data")
    df = pd.DataFrame(json_data['features'], columns=["AT", "V", "AP", "RH"])
    pre = run_model_tarining.predict_lr(df)
    result_data["predict_res"] = json.dumps(pre, cls=MyEncoder)
    result_data["success"] = True
    return  str(result_data)


@app.route("/test", methods=["POST"])
def test():
    """项目演示示例"""
    try:
        #训练次数
        steps = flask.request.form["steps"]
        res = run_model_tarining.train(steps=int(steps))
        return "succeed"
    except:
        return "请求参数异常！"


# 本地开发调试用，如果部署到生成环境，请使用ngnix Tomcat
if __name__ == "__main__":
    print("* Starting web service...")
    app.run()

