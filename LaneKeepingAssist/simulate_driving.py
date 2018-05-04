import cv2
import numpy as np
import argparse
import os
from steering_model import SteeringModel
from utility import load_image, radian2degree

steering_model = None

def simulate_driving(args):
    f = open(os.path.join(args.data_dir, 'data.txt'), 'r')
    wheel_img = cv2.imread('wheel.jpg', 0)
    rows, cols = wheel_img.shape

    for line in f:
        image = load_image(args.data_dir, line.split()[0])
        cv2.imshow('image', image)
        steering_radian = steering_model.predict(image)
        steering_degree = radian2degree(steering_radian)

        M = cv2.getRotationMatrix2D((cols/2, rows/2), -2*steering_degree, 1)
        dst = cv2.warpAffine(wheel_img, M, (cols, rows))
        cv2.imshow("wheel", dst)

        key = cv2.waitKey(10)

        if key & 0xFF == ord('q'):
            break
            cv2.destroyAllWindows()


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Simulate Driving')
    parser.add_argument('-m', help='path to model h5 file.', dest='model', type=str, default='model.h5')
    parser.add_argument('-d', help='data directory',         dest='data_dir', type=str, default='data')
    args = parser.parse_args()

    steering_model = SteeringModel()
    steering_model.load_model_from(args.model)
    simulate_driving(args)
