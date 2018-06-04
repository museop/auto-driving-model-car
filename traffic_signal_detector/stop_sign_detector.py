import os
import cv2
import numpy as np


QUEUE_SIZE = 30
THRESHHOLD = 1

DEFAULT_HAAR_PATH = os.path.join(os.path.dirname(__file__), "resources", "stop_sign.xml")


class StopSignDetector(object):
    def __init__(self, cascade_classifier=DEFAULT_HAAR_PATH):
        self.font = cv2.FONT_HERSHEY_SIMPLEX
        self.stopsign_cascade = cv2.CascadeClassifier(cascade_classifier)
        self.queue = []
        self.num_true_in_queue = 0
        for i in range(QUEUE_SIZE):
            self.queue.append(False)
    
    def detect(self, image):
        """
        Detect the stop signs from the image(BGR image).
        """
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        stop_signs = self.stopsign_cascade.detectMultiScale(gray)
        
        detections = []
        for (x_pos, y_pos, width, height) in stop_signs:
            #cv2.putText(image, 'Stop!', (x_pos-5, y_pos-5), self.font, 0.5, (0, 0, 255), 2)
            #cv2.rectangle(image, (x_pos, y_pos), (x_pos+width, y_pos+height), (0, 0, 255), 2)
            detections.append((x_pos, y_pos, width, height))

        return detections

    def determine_the_status(self, image):
        """
        Determine the status from the image(BGR image).
        """
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        stop_signs = self.stopsign_cascade.detectMultiScale(gray)

        if len(stop_signs) > 0:
            x = self.queue.pop(0)
            if x == False:
                self.num_true_in_queue += 1
            self.queue.append(True)
        else:
            x = self.queue.pop(0)
            if x == True:
                self.num_true_in_queue -= 1
            self.queue.append(False)

        return self.num_true_in_queue >= THRESHHOLD
        
