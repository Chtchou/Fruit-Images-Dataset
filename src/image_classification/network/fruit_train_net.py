import tensorflow as tf
import numpy as np
import time

from network_structure import fruit_network as network
from network_structure import utils

from utils import constants

# number of iterations to run the training
iterations = 20000
# amount of iterations after we display the loss and accuracy
display_interval = 50
# use the saved model and continue training
useCkpt = True
# placeholder for probability to keep the network parameters after an iteration
keep_prob = tf.placeholder(tf.float32, name='keep_prob')


# prepare the input tensors for the network
def inputs(filename, batch_size):
    image, label = utils.read_file(filename)
    image = utils.adjust_image_for_train(image)
    images, labels = tf.train.shuffle_batch([image, label],
                                            batch_size=batch_size,
                                            capacity=30000 + batch_size,
                                            min_after_dequeue=10000)
    return images, labels


logits = network.conv_net(network.X, network.weights, network.biases, keep_prob)
prediction = tf.nn.softmax(logits)

loss_operation = tf.reduce_mean(tf.nn.sparse_softmax_cross_entropy_with_logits(logits=logits,
                                                                               labels=network.Y))

optimizer = tf.train.AdamOptimizer(learning_rate=network.learning_rate)
train_op = optimizer.minimize(loss=loss_operation)

correct_prediction = tf.equal(tf.argmax(prediction, 1), network.Y)
accuracy = tf.reduce_mean(tf.cast(correct_prediction, tf.float32))

init = tf.global_variables_initializer()


def train_model():
    global learning_rate
    time1 = time.time()
    for i in range(1, iterations + 1):
        with tf.Graph().as_default():

            batch_x, batch_y = sess.run([images, labels])
            batch_x = np.reshape(batch_x, [network.batch_size, network.input_size])

            sess.run(train_op, feed_dict={network.X: batch_x, network.Y: batch_y, keep_prob: network.dropout})

            if i % display_interval == 0 or i == 1:
                loss, acc = sess.run([loss_operation, accuracy], feed_dict={network.X: batch_x, network.Y: batch_y, keep_prob: 1})
                learning_rate = update_learning_rate(acc, learn_rate=network.initial_learning_rate)
                # save the weights and the meta data for the graph
                saver.save(sess, constants.fruit_models_dir + 'model.ckpt')
                tf.train.write_graph(sess.graph_def, constants.fruit_models_dir, 'graph.pbtxt')
                time2 = time.time()
                print("time: %.4f step: %d loss: %.4f accuracy: %.4f" % (time2 - time1, i, loss, acc))
                time1 = time.time()


def update_learning_rate(acc, learn_rate):
    return learn_rate - acc * learn_rate * 0.9


saver = tf.train.Saver()

with tf.Session() as sess:
    sess.run(init)
    # input tfrecord file
    tfrecords_name = constants.data_dir + 'train-00000-of-00001'
    images, labels = inputs(tfrecords_name, network.batch_size)
    coord = tf.train.Coordinator()
    threads = tf.train.start_queue_runners(sess=sess, coord=coord)

    # restore the previously saved value if we wish to continue the training
    if useCkpt:
        ckpt = tf.train.get_checkpoint_state(constants.fruit_models_dir)
        saver.restore(sess, ckpt.model_checkpoint_path)

    train_model()

    coord.request_stop()
    coord.join(threads)
    sess.close()
