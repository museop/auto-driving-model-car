import tensorflow as tf
from cnn_model import CNN_Model 
from data_reader import DataReader 

BATCH_SIZE = 100
LEARNING_RATE = 1e-4
L2_REG = 0.001
STAGES = 30

def main():
    global_step = tf.Variable(0, trainable=False, name='global_step')

    model = CNN_Model()

    train_vars = tf.trainable_variables()
    cost = tf.sqrt(tf.reduce_mean(tf.square(tf.subtract(model.y_, model.y))) + tf.add_n([tf.nn.l2_loss(v) for v in train_vars]) * L2_REG)
    optimizer = tf.train.AdamOptimizer(LEARNING_RATE)
    train_op = optimizer.minimize(cost, global_step=global_step)

    sess = tf.Session()
    saver = tf.train.Saver(tf.global_variables())

    ckpt = tf.train.get_checkpoint_state('./model')
    if ckpt and tf.train.checkpoint_exists(ckpt.model_checkpoint_path):
        print(ckpt.model_checkpoint_path)
        saver.restore(sess, ckpt.model_checkpoint_path)
    else:
        sess.run(tf.global_variables_initializer())
    
    data_reader = DataReader()

    for stage in range(STAGES):
        for i in range(int(data_reader.num_images / BATCH_SIZE)):
            xs, ys = data_reader.load_train_batch(BATCH_SIZE)
            sess.run(train_op, feed_dict={ model.x: xs, model.y_: ys, model.keep_prob: 0.8 })
            g_step = sess.run(global_step)
            train_cost = sess.run(cost, feed_dict={ model.x: xs, model.y_: ys, model.keep_prob: 1.0 })
            print('Step: %d,' % g_step, 'Train Cost: %.3f' % train_cost)

            if i % 10 == 0:
                xs, ys = data_reader.load_val_batch(BATCH_SIZE)
                val_cost = sess.run(cost, feed_dict={ model.x: xs, model.y_: ys, model.keep_prob: 1.0 })
                print('Step: %d, Val Cost %g' % (g_step, val_cost))

        saver.save(sess, './model/model.ckpt', global_step=global_step)
    print('done.')

if __name__ == '__main__':
    main()
