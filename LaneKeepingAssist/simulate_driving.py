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

    lines = f.readlines()

    num_of_frames = len(lines)
    if args.start_index >= num_of_frames:
        print('start index is too large.. (start index: %d, num of frames: %d)' % (start_index, num_of_frames))
    for i in range(args.start_index, num_of_frames, 1):
        image = load_image(args.data_dir, lines[i].split()[0])
        steering_radian = steering_model.predict(image)
        steering_degree = radian2degree(steering_radian)

        M = cv2.getRotationMatrix2D((cols/2, rows/2), -2*steering_degree, 1)
        dst = cv2.warpAffine(wheel_img, M, (cols, rows))
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
        image = cv2.resize(image, None, fx=2, fy=2, interpolation=cv2.INTER_CUBIC)
        cv2.imshow('image', image)
        cv2.imshow("wheel", dst)

        key = cv2.waitKey(10)

        if key & 0xFF == ord('q'):
            cv2.destroyAllWindows()
            break

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Simulate Driving')
    parser.add_argument('-m', help='path to model h5 file.', dest='model',       type=str, default='model.h5')
    parser.add_argument('-d', help='data directory',         dest='data_dir',    type=str, default='data')
    parser.add_argument('-i', help='start index',            dest='start_index', type=int, default=0)
    args = parser.parse_args()

    steering_model = SteeringModel()
    steering_model.load_model_from(args.model)
    simulate_driving(args)
