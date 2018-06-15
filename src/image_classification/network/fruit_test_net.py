import numpy
import tensorflow as tf
import numpy as np
import os

from network_structure import fruit_network as network
from network_structure import utils
from utils import constants

checkpoint_dir = os.getcwd() + '\\..\\fruit_models\\'
keep_prob = tf.placeholder(tf.float32)

images_left_to_process = 9673
# total number of images used to test
total_test_images = 9673

# create a map to add for each label the amount of images that were labeled incorrectly
mislabeled = {}

# associate the label number with the actual human readable label name
with open(constants.data_dir + 'labels') as f:
    labels_text = f.readlines()
labels_text = [x.strip() for x in labels_text]
for label in labels_text:
    mislabeled[label] = 0

# class 0 is background class so it's labeled as nothing
labels_text = ["nothing"] + labels_text


def inputs(filename, batch_size):
    image, label = utils.read_file(filename)
    image = utils.adjust_image_for_test(image)
    images, labels = tf.train.batch([image, label],
                                    batch_size=batch_size,
                                    capacity=total_test_images + batch_size)
    return images, labels


def test_model():
    global images_left_to_process
    correct = 0
    while images_left_to_process > 0:
        batch_x, batch_y = sess.run([images, labels])
        batch_x = np.reshape(batch_x, [network.batch_size, network.input_size])
        # the results of the classification is an array of 1 and 0, 1 is a correct classification
        results = sess.run(correct_pred, feed_dict={network.X: batch_x, network.Y: batch_y, keep_prob: 1})
        images_left_to_process = images_left_to_process - network.batch_size
        for i in range(len(results)):
            if not results[i]:
                mislabeled[labels_text[batch_y[i]]] += 1

        correct = correct + numpy.sum(results)
        print("Predicted %d out of %d; partial accuracy %.4f" % (correct, total_test_images - images_left_to_process, correct / (total_test_images - images_left_to_process)))
    print(correct / total_test_images)


logits = network.conv_net(network.X, network.weights, network.biases, keep_prob)
prediction = tf.nn.softmax(logits)

loss_op = tf.reduce_mean(tf.nn.sparse_softmax_cross_entropy_with_logits(logits=logits,
                                                                        labels=network.Y))
optimizer = tf.train.AdamOptimizer(learning_rate=network.learning_rate)
train_op = optimizer.minimize(loss=loss_op)

correct_pred = tf.equal(tf.argmax(prediction, 1), network.Y)
accuracy = tf.reduce_mean(tf.cast(correct_pred, tf.float32))

init = tf.global_variables_initializer()


saver = tf.train.Saver()

with tf.Session() as sess:
    sess.run(init)
    tfrecords_name = constants.data_dir + 'validation-00000-of-00001'
    images, labels = inputs(tfrecords_name, network.batch_size)
    coord = tf.train.Coordinator()
    threads = tf.train.start_queue_runners(sess=sess, coord=coord)

    ckpt = tf.train.get_checkpoint_state(checkpoint_dir)
    saver.restore(sess, ckpt.model_checkpoint_path)

    test_model()
    print(mislabeled)

    coord.request_stop()
    coord.join(threads)
    sess.close()
