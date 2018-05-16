import enum
from abc import ABCMeta
from abc import abstractmethod


class UserEventType(enum.Enum):
    DEFAULT = 0
    MODE_ON = 1
    MODE_OFF = 2
    MOVE_FRONT = 3
    MOVE_BACK = 4
    BRAKE = 5
    SPEED_UP = 6
    SPEED_DOWN = 7
    CHANGE_STEERING_ANGLE = 8
    EXIT_PROGRAM = 9


class UserInputDevice:
    __metaclass__ = ABCMeta

    @abstractmethod
    def device_name(self):
        raise NotImplementedError

    @abstractmethod
    def is_available(self):
        raise NotImplementedError

    @abstractmethod
    def read_user_event(self):
        raise NotImplementedError


