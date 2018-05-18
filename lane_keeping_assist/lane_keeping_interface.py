from abc import ABCMeta
from abc import abstractmethod


class ILaneKeeping:
    __metaclass__ = ABCMeta

    @abstractmethod
    def setup_frame_color_space(self, color_space):
        raise NotImplementError

    @abstractmethod
    def predict_angle(self, front_frame):
        raise NotImplementError

