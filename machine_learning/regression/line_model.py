import tensorflow as tf 
import numpy as np 

def line_model():
    # Set Feature item
    installed_capacity = np.array([[300],[250],[280],[310],[260],[270],[330],[290],[285],[261]]).astype(np.float32)
    water_level = np.array([[311],[309],[320],[290],[281],[295],[301],[288],[304],[322]]).astype(np.float32)
    water_volume = np.array([[30],[29],[25],[32],[35],[33],[31],[28],[24],[27]]).astype(np.float32)
    temperature = np.array([[15],[18],[16],[20],[25],[28],[25],[22],[23],[26]]).astype(np.float32)
    generated_electrical_energy = np.array([[210],[200],[190],[195],[200],[198],[215],[180],[180],[250]]).astype(np.float32)

    x_test_installed_capacity = installed_capacity[0:5].reshape(-1,1)
    x_test_water_level = water_level[0:5].reshape(-1,1)
    x_test_water_volume = water_volume[0:5].reshape(-1,1)
    x_test_temperature = temperature[0:5].reshape(-1,1)
    y_test_generated_electrical_energy = generated_electrical_energy[0:5]
    x_train_installed_capacity = installed_capacity[5:].reshape(-1,1)
    x_train_water_level = water_level[5:].reshape(-1,1)
    x_train_water_volume = water_volume[5:].reshape(-1,1)
    x_train_temperature = temperature[5:].reshape(-1,1)
    y_train_generated_electrical_energy = generated_electrical_energy[5:]

    x_installed_capacity = tf.placeholder(tf.float32,[None,1])
    x_water_level = tf.placeholder(tf.float32,[None,1])
    x_water_volume = tf.placeholder(tf.float32,[None,1])
    x_temperature = tf.placeholder(tf.float32,[None,1])
    w_installed_capacity = tf.Variable(tf.zeros([1,1]))
    w_water_level = tf.Variable(tf.zeros([1,1]))
    w_water_volume = tf.Variable(tf.zeros([1,1]))
    w_temperature =  tf.Variable(tf.zeros([1,1]))
    b = tf.Variable(tf.zeros([1]))

    y = tf.matmul(x_installed_capacity,w_installed_capacity) + tf.matmul(x_water_level,w_water_level) + tf.matmul(x_water_volume,w_water_volume) + tf.matmul(x_temperature,w_temperature) + b
    y_ = tf.placeholder(tf.float32,[None,1])
    cost = tf.reduce_mean(tf.square(y_ - y))
    train_step = tf.train.GradientDescentOptimizer(0.000001).minimize(cost)
    init = tf.global_variables_initializer()
    saver = tf.train.Saver()
    sess = tf.Session()
    sess.run(init)
    cost_history = []

    for i in range(1000):
        feed = {x_installed_capacity:x_train_installed_capacity,x_water_level:x_train_water_level,x_water_volume:x_train_water_volume,x_temperature:x_train_temperature,y_:y_train_generated_electrical_energy}
        sess.run(train_step,feed_dict = feed)
        cost_history.append(sess.run(cost,feed_dict = feed))
        print("After %d iteration:" %i)
        print("w_installed_capacity: %f" %sess.run(w_installed_capacity))
        print("w_water_level: %f" %sess.run(w_water_level))
        print("w_water_volume: %f" %sess.run(w_water_volume))
        print("w_temperature: %f" %sess.run(w_temperature))
        print("b: %f" %sess.run(b))
        print("cost: %f" %sess.run(cost,feed_dict = feed))

    print("w_installed_capacity: %f" %
        sess.run(w_installed_capacity),"w_water_level: %f" %
        sess.run(w_water_level),"w_water_volume: %f" %
        sess.run(w_water_volume),"w_temperature: %f" %
        sess.run(w_temperature),"b: %f" %
        sess.run(b),"cost: %f" % sess.run(cost, feed_dict = feed))

    saver_path = saver.save(sess, "../regression/model/model.ckpt")
    print("Model saved in file:", saver_path)

def load_model(x_ic, x_wl, x_wv, x_t):
    x_installed_capacity = tf.placeholder(tf.float32,[None,1])
    x_water_level = tf.placeholder(tf.float32,[None,1])
    x_water_volume = tf.placeholder(tf.float32,[None,1])
    x_temperature = tf.placeholder(tf.float32,[None,1])
    w_installed_capacity = tf.Variable(tf.zeros([1,1]))
    w_water_level = tf.Variable(tf.zeros([1,1]))
    w_water_volume = tf.Variable(tf.zeros([1,1]))
    w_temperature =  tf.Variable(tf.zeros([1,1]))
    b = tf.Variable(tf.zeros([1]))
    y = tf.matmul(x_installed_capacity,w_installed_capacity) + tf.matmul(x_water_level,w_water_level) + tf.matmul(x_water_volume,w_water_volume) + tf.matmul(x_temperature,w_temperature) + b

    saver = tf.train.Saver()
    with tf.Session() as sess:    
        saver.restore(sess, "../regression/model/model.ckpt")
        return  sess.run(y, feed_dict={x_installed_capacity:[[x_ic]], 
            x_water_level:[[x_wl]], x_water_volume:[[x_wv]], x_temperature:[[x_t]]})

#line_model()
print("y value is:%f" %load_model(315,290,25,23))
