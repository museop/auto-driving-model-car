import cv2
import numpy as np
import argparse
import os
import time
from lane_keeping import LaneKeeping
from utils import radian2degree
from utils import load_image


def simulate_driving(args):
    lane_keeping_assist = LaneKeeping()
    lane_keeping_assist.setup_frame_color_space("rgb")

    f = open(os.path.join(args.data_dir, 'data.txt'), 'r')
    wheel_img = cv2.imread('wheel.jpg', 0)
    rows, cols = wheel_img.shape

    lines = f.readlines()
    num_of_frames = len(lines)
    if args.start_index >= num_of_frames:
        print('start index is too large.. (start index: %d, num of frames: %d)' % (start_index, num_of_frames))
    for i in range(args.start_index, num_of_frames, 1):
        start_time = time.time()

        image = load_image(args.data_dir, lines[i].split()[0])

        steering_radian = lane_keeping_assist.predict_angle(image)
        steering_degree = radian2degree(steering_radian)

        M = cv2.getRotationMatrix2D((cols/2, rows/2), -2*steering_degree, 1)
        dst = cv2.warpAffine(wheel_img, M, (cols, rows))

        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
        image = cv2.resize(image, None, fx=2, fy=2, interpolation=cv2.INTER_CUBIC)

        fps = 1 / (time.time() - start_time)
        text = "Steering angle: %f radian.\nFPS: %.02f" % (steering_radian, fps)

        y0, dy = 30, 30
        for j, line in enumerate(text.split('\n')):
            y = y0 + j*dy
            image = cv2.putText(image, line, (20, y), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
        cv2.imshow('image', image)
        cv2.imshow("wheel", dst)

        key = cv2.waitKey(10)
        if key & 0xFF == ord('q'):
            cv2.destroyAllWindows()
            break
        elif key & 0xFF == ord('s'):
            cv2.imwrite(str(i) + '.jpg', image)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Simulate Driving')
    parser.add_argument('-d', help='data directory',         dest='data_dir',    type=str, default='data')
    parser.add_argument('-i', help='start index',            dest='start_index', type=int, default=0)
    args = parser.parse_args()

    simulate_driving(args)
    

