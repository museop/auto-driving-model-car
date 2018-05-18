from abc import ABCMeta
from abc import abstractmethod


class IAutoDriving:
    __metaclass__ = ABCMeta

    @abstractmethod
    def auto_driving_mode(self, mode):
        raise NotImplementedError

    @abstractmethod
    def speed_up(self, value):
        raise NotImplementedError

    @abstractmethod
    def speed_down(self, value):
        raise NotImplementedError

    @abstractmethod
    def steer_wheel(self, steering_radian):
        raise NotImplementedError

    @abstractmethod
    def move_front(self):
        raise NotImplementedError

    @abstractmethod
    def move_back(self):
        raise NotImplementedError

    @abstractmethod
    def clear(self):
        raise NotImplementedError
        
    @abstractmethod
    def brake(self):
        raise NotImplementedError

