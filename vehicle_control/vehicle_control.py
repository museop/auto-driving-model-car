from abc import ABCMeta
from abc import abstractmethod


class IVehicleControl:
    __metaclass__ = ABCMeta

    @abstractmethod
    def move_front(self, pwm):
        raise NotImplementedError

    @abstractmethod
    def move_back(self, pwm):
        raise NotImplementedError

    @abstractmethod
    def steer_wheel(self, radian):
        raise NotImplementedError

    @abstractmethod
    def stop(self):
        raise NotImplementedError

