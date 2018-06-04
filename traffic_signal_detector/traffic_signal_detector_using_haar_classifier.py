import time
import numpy as np
from traffic_signal_detect import ITrafficSignalDetect
from stop_sign_detector import StopSignDetector
from traffic_light_detector import TrafficLightDetector


class TrafficSignalDetectorUsingHAARClassifier(ITrafficSignalDetect):
    def __init__(self):
        super(TrafficSignalDetectorUsingHAARClassifier, self).__init__()
        print('init TrafficSignalDetector')
        self.stop_sign_detector = StopSignDetector()
        self.traffic_light_detector = TrafficLightDetector()

    def can_go_forward(self, frame, low_accuracy):
        is_there_a_stop_sign = self.stop_sign_detector.determine_the_status(frame)
        if is_there_a_stop_sign:
            return False

        color_of_traffic = self.traffic_light_detector.determine_the_status(frame)
        if color_of_traffic == "red" or color_of_traffic == "yellow":
            return False

        return True
    
    def detect(self, frame):
        stop_signs = self.stop_sign_detector.detect(frame)
        traffic_lights = self.traffic_light_detector.detect(frame)
        res = []

        for i in range(len(stop_signs)):
            x, y, w, h = stop_signs[i]
            res.append(('stop sign', int((x+x+w)/2), int((y+y+h)/2), w, h))

        for i in range(len(traffic_lights)):
            x, y, w, h, name = traffic_lights[i]
            res.append((name, int((x+w)/2), int((y+h)/2), w, h))

        return res

    def visualize_traffic_info(self, frame):
        detected_objs = self.detect(frame)
        num_objs = len(detected_objs)

        for i in range(num_objs):
            label, x, y, width, height = detected_objs[i]
            x1 = int(x-width/2)
            y1 = int(y-height/2)
            x2 = int(x+width/2)
            y2 = int(y+height/2)
            cv2.putText(frame, label, (x1-5, y1-5), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255))
            cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 0, 255), 2)
        return frame
        
    def avg_processing_time(self, frame_height, frame_width):
        img = np.ones((frame_height,frame_width,3), np.uint8) * 255
        self.detect(img) # The initial detecting time is excluded.

        h, w = img.shape[:2]

        colors = [(255, 0, 0), (0, 255, 0), (0, 0, 255), (0, 0, 0), (255, 255, 255)]
        num_iterations = len(colors)

        sum_time = 0.0
        for i in range(num_iterations):
            for y in range(h):
                for x in range(w):
                    img[y][x] = colors[i]
            start_time = time.time()
            self.detect(img)
            sum_time = sum_time + (time.time() - start_time)

        avg_time = sum_time/num_iterations
        return avg_time
        
    def __del__(self):
        print('delete TrafficSignalDetectorUsingHAARClassifier')


if __name__ == '__main__':
    import cv2
    cap = cv2.VideoCapture("nvcamerasrc ! video/x-raw(memory:NVMM), width=(int)%d, height=(int)%d,format=(string)I420, framerate=(fraction)30/1 ! nvvidconv flip-method=0 ! video/x-raw, format=(string)BGRx ! videoconvert ! video/x-raw, format=(string)BGR ! appsink"%(320, 160))
    
    detector = TrafficSignalDetectorUsingHAARClassifier()
    print(detector.avg_processing_time(160, 320))
    while cap.isOpened():
        ret, frame = cap.read()
        # camera calibration required if you detect traffic lights.
        frame = detector.visualize_traffic_info(frame)
        cv2.imshow('frame', frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    cv2.destroyAllWindows()
