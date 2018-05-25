import flask
from flask import Flask, jsonify
from flask_cors import CORS
app = Flask(__name__)
CORS(app, supports_credentials=True)

tasks = [
    {
        'id': 1,
        'title': u'Buy groceries',
        'description': u'Milk, Cheese, Pizza, Fruit, Tylenol',
        'done': False
    },
    {
        'id': 2,
        'title': u'Learn Python',
        'description': u'Need to find a good Python tutorial on the web',
        'done': False
    }]


@app.route('/')
def index():
    return 'Hello,This is my api address!'


@app.route('/todo/api/v1.0/tasks', methods=['GET'])
def get_tasks():
    return jsonify({'tasks': tasks})

@app.route('/test',methods=['POST'])
def test():
    tmp=flask.request.form["features"]
    print(tmp)
    return "succeed"
if __name__=="__main__":
    app.run()