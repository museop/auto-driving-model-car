import os
import cv2
from steering_model import SteeringModel
from lane_keeping_interface import ILaneKeeping


MODEL_PATH = os.path.join(os.path.dirname(__file__), "model.h5")


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
    
    def __del__(self):
        print('delete LaneKeeping')
        
