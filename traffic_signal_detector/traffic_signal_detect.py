from abc import ABCMeta
from abc import abstractmethod


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

