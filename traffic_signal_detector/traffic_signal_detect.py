from abc import ABCMeta
from abc import abstractmethod


class ITrafficSignalDetect:
    __metaclass__ = ABCMeta

    @abstractmethod
    def detect(self, frame):
        raise NotImplementedError

    @abstractmethod
    def can_go_forward(self, low_accuracy):
        raise NotImplementedError
        
    @abstractmethod
    def visualize_traffic_info(self, frame):
        raise NotImplementedError
        
    @abstractmethod
    def avg_processing_time(self, frame_height, frame_width):
        raise NotImplementedError
