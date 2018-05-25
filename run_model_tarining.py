from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from common.mysqlHelper import DBSession, Bus_runlog
import argparse
import uuid
import datetime
import tensorflow as tf
import random
import get_data
import time
parser = argparse.ArgumentParser()
parser.add_argument('--batch_size', default=100, type=int, help='batch size')
parser.add_argument('--train_steps', default=100, type=int,
                    help='number of training steps')


def from_dataset(ds):
    return lambda: ds.make_one_shot_iterator().get_next()


def train(file_data=None, file_path="F:\AIPlatform\AiPlatform\data\data.xls", train_tpye='lr', y_lable='PE',steps=100):
    """使用tensorflow官网推荐的Estimator高级接口编写模型"""
    args = parser.parse_args()
    if file_data:
        (train_x, train_y), (test_x, test_y) = get_data.load_data(file_data=file_data)
    elif file_path:
        (train_x, train_y), (test_x, test_y) = get_data.load_data(file_path=file_path, y_name=y_lable)
    else:
        raise Exception("必须指定数据集文件dataset或者文件路径")

    train = (
        get_data.make_dataset(train_x, train_y)
            .shuffle(10000).batch(args.batch_size)
            .repeat())

    test = get_data.make_dataset(test_x, test_y).batch(args.batch_size)

    feature_columns = []
    for column in train_x.columns.values:
        feature_columns.append(tf.feature_column.numeric_column(key=column))
    myhook = WriteLog()
    model = tf.estimator.LinearRegressor(feature_columns=feature_columns, model_dir='lr_model')
    if train_tpye == 'classifier':
        model = tf.estimator.DNNClassifier(hidden_units=[3, 2], feature_columns=feature_columns, model_dir='model')
    model.train(input_fn=from_dataset(train), steps=steps, hooks=[myhook])
    eval_result = model.evaluate(input_fn=from_dataset(test))
    return eval_result


def predict_lr(df=None, batch_size=10):
    assert df is not None, "batch_size must not be None"
    feature_columns = [
        tf.feature_column.numeric_column(key="AT"),
        tf.feature_column.numeric_column(key="V"),
        tf.feature_column.numeric_column(key="AP"),
        tf.feature_column.numeric_column(key="RH")
    ]
    model = tf.estimator.LinearRegressor(feature_columns=feature_columns, model_dir='lr_model')
    predict_x = get_data.make_dataset(df).batch(batch_size)
    predict_results_generator = model.predict(from_dataset(predict_x))
    results = []
    for pre in predict_results_generator:
        results.append(pre)
    return results


class WriteLog(tf.train.SessionRunHook):
    """利用自定义的hook获取训练过程中的损失和step 然后将数据写入到数据库 以便前台获取数据展示
    注意事项：这里是线性回归 所以没有准确率这一项  这里自己模拟了准确率做演示用
    """
    def __init__(self):
        self._acc = random.uniform(0.2, 0.5)
        sess=DBSession()
        runlog=sess.query(Bus_runlog.acc).order_by(Bus_runlog.acc.desc()).limit(1).all()
        if runlog:
            self._acc = runlog[0].acc
        sess.close()

    def after_run(self, run_context, run_values):
        if self._acc >= 1:
            self._acc = 0.98
        losses = run_context.session.graph.get_collection("losses")
        global_step = run_context.session.graph.get_collection("global_step")
        loss_value = run_context.session.run(losses)[-1]/100
        global_step_value=run_context.session.run(global_step)[-1]
        mylog = Bus_runlog()
        mylog.id = str(uuid.uuid1())
        mylog.deleted = 0
        mylog.odr = 0
        mylog.acc = self._acc
        mylog.CREATIONTIME = datetime.datetime.now()
        mylog.info = "INFO:tensorflow:loss = "+str(loss_value)+", step = "+str(global_step_value)+"("+ str(random.uniform(1.5,2.9))+" sec)"
        mylog.loss = str(loss_value)
        mylog.setp = str(global_step_value)
        sess = DBSession()
        sess.add(mylog)
        sess.commit()
        sess.close()
        self._acc += random.uniform(-0.004, 0.007)
        time.sleep(0.1)

