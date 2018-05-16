from abc import ABCMeta
from abc import abstractmethod


class Camera:
    __metaclass__ = ABCMeta

    @abstractmethod
    def open(self):
        raise NotImplementedError

    @abstractmethod
    def is_opened(self):
        raise NotImplementedError

    @abstractmethod
    def capture_frame(self):
        raise NotImplementedError

    @abstractmethod
    def calibrate(self, frame):
        raise NotImplementedError
        
    @abstractmethod    
    def save_frame(self, directory, filename, frame):
        raise NotImplementedError

