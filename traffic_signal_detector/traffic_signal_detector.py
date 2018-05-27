from abc import ABCMeta
from abc import abstractmethod
from stop_sign_detector import StopSignDetector
from traffic_light_detector import TrafficLightDetector


class ITrafficSignalDetect:
    __metaclass__ = ABCMeta

    @abstractmethod
    def detect_stop_signs(self, front_frame):
        raise NotImplementedError

    @abstractmethod
    def detect_traffic_lights(self, front_frame):
        raise NotImplementedError

    @abstractmethod
    def can_go_forward(self, front_frame):
        raise NotImplementedError


class TrafficSignalDetector(ITrafficSignalDetect):
    def __init__(self):
        super(TrafficSignalDetector, self).__init__()
        print('init TrafficSignalDetector')
        self.stop_sign_detector = StopSignDetector()
        self.traffic_light_detector = TrafficLightDetector()

    def detect_stop_signs(self, front_frame):
        frame = self.stop_sign_detector.detect(front_frame)
        return frame

    def detect_traffic_lights(self, front_frame):
        frame = self.traffic_light_detector.detect(front_frame)
        return frame

    def can_go_forward(self, front_frame):
        is_there_a_stop_sign = self.stop_sign_detector.determine_the_status(front_frame)
        if is_there_a_stop_sign:
            return False

        color_of_traffic = self.traffic_light_detector.determine_the_status(front_frame)
        if color_of_traffic == "red" or color_of_traffic == "yellow":
            return False

        return True

        
