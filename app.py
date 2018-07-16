#!usr/bin/env python  
# -*- coding:utf-8 _*-
""" 
@Author:jayden 
@File: app.py 
@Time: 2018/07/05 
"""
from flask import Flask, jsonify
from flasgger import Swagger
from flask_cors import CORS
import redis
import settings
import algorithms.statistics.sta as sta
app = Flask(__name__)
CORS(app, supports_credentials=True)
swagger = Swagger(app)
db=redis.StrictRedis(settings.REDIS_HOST,settings.REDIS_PORT,settings.REDIS_DB)


@app.route("/")
def index():
    return "东电科技数据挖掘算法平台"


@app.route("/api/statistical/covariance/<data>", methods=["POST"])
def covariance(data):
    """计算特征数据集的协方差矩阵
        ---
        parameters:
          - name: data
            in: path
            type: string
            description: "需要计算的特征数据表"
            required: true
        responses:
          200:
            description: 原特征集的协方差矩阵
        """
    df=sta.correlation(data=data)
    return jsonify(df)


if __name__ == "__main__":
    app.run(debug=True)
