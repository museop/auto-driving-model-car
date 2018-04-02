import tensorflow as tf
import cv2
import scipy.misc
from cnn_model import CNN_model

DATASET_DIR = '/home/nvidia/Desktop/Workspace/driving_dataset/'

class NeuralNetwork(object):
    
    def __init__(self):
        self.model = CNN_model()
        self.sess = tf.Session()
        
    def load(self, ckpt_path):
        saver = tf.train.Saver()
        saver.restore(self.sess, ckpt_path)

    def predict(self, img):
        value = self.model.predict(self.sess, img)
        return value

if __name__ == "__main__":
    
    network = NeuralNetwork()
    network.load('save/model.ckpt')

    hangle_img = cv2.imread('steering_wheel_image.jpg', 0)
    rows, cols = hangle_img.shape
    
    smoothed_angle = 0
    i = 0
    while cv2.waitKey(10) != ord('q'):
        full_img = scipy.misc.imread(DATASET_DIR + str(i) + ".jpg", mode="RGB")
        cv2.imshow('full_img', cv2.cvtColor(full_img, cv2.COLOR_RGB2BGR))
        degree = network.predict(full_img) * 180.0 / scipy.pi

        smoothed_angle += 0.2 * pow(abs(degree - smoothed_angle), 2.0 / 3.0) * (degree - smoothed_angle) / abs(degree - smoothed_angle)
        print("Frame id: %d, Predicted angle: %f" % (i, smoothed_angle))
#        M = cv2.getRotationMatrix2D((cols/2, rows/2), -smoothed_angle, 1)
#        dst = cv2.warpAffine(hangle_img, M, (cols, rows))
#        cv2.imshow('steering wheel', dst)
        i += 1

    cv2.destroyAllWindows()


