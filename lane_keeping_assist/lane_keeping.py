import os
import time
import numpy as np
import cv2
from abc import ABCMeta
from abc import abstractmethod
from steering_model import SteeringModel


class ILaneKeeping:
    __metaclass__ = ABCMeta

    @abstractmethod
    def setup_frame_color_space(self, color_space):
        raise NotImplementError

    @abstractmethod
    def predict_angle(self, front_frame):
        raise NotImplementError

    @abstractmethod
    def avg_processing_time(self, frame_height, frame_width):
        raise NotImplementError


MODEL_PATH = os.path.join(os.path.dirname(__file__), "steering_model-010.h5")


class LaneKeeping(ILaneKeeping):
    """
    LaneKeeping Class
    This class helps the vehicle not leave the lane.
    """
    def __init__(self):
        super(LaneKeeping, self).__init__()
        print('init LaneKeeping')
        self.steering_model = SteeringModel()
        self.frame_color_space = "BGR"

    def setup_frame_color_space(self, color_space):
        """
        Setup the related setting and load resources for lane keeping.
        """
        if color_space != 'rgb' and color_space != 'bgr':
            print('The color format of frame must be rgb or bgr.')
            return
        self.frame_color_space = color_space
        self.steering_model.load_model_from(MODEL_PATH)

    def predict_angle(self, front_frame):
        """
        Predict the steering angle(radian) to keep the lane.
        """
        if self.frame_color_space == "bgr":
            front_frame = cv2.cvtColor(front_frame, cv2.COLOR_BGR2RGB)
        steering_angle = self.steering_model.predict(front_frame)
        return steering_angle

    def avg_processing_time(self, frame_height, frame_width):
	img = np.ones((frame_height,frame_width,3), np.uint8) * 255
        self.predict_angle(img) # The initial detecting time is excluded.

        h, w = img.shape[:2]

        colors = [(255, 0, 0), (0, 255, 0), (0, 0, 255), (0, 0, 0), (255, 255, 255)]
        num_iterations = len(colors)

        sum_time = 0.0
        for i in range(num_iterations):
            for y in range(h):
                for x in range(w):
                    img[y][x] = colors[i]
            start_time = time.time()
            self.predict_angle(img)
            sum_time = sum_time + (time.time() - start_time)

        avg_time = sum_time/num_iterations
        return avg_time
    
    def __del__(self):
        print('delete LaneKeeping')
        
