import cv2
import numpy as np 

RED_MIN = np.array([-10, 100, 100])
RED_MAX = np.array([10, 255, 255])

YELLOW_MIN = np.array([15, 100, 100])
YELLOW_MAX = np.array([40, 255, 255])

GREEN_MIN = np.array([50, 100, 50])
GREEN_MAX = np.array([120, 255, 255])

QUEUE_SIZE = 20

UNKNOWN, RED, YELLOW, GREEN = 0, 1, 2, 3
COLORS_NAME = ["unknown", "red", "yellow", "green"]
COLORS = [(0, 0, 0), (0, 0, 255), (0, 255, 255), (0, 255, 0)]

def argmax(a_list):
    len_list = len(a_list)
    max_value = 0
    argmax_i = 0
    for i in range(len_list):
        if a_list[i] > max_value:
            max_value = a_list[i]
            argmax_i = i
    return argmax_i


class TrafficLightDetector(object):
    def __init__(self, cascade_classifier='TrafficLight_HAAR.xml'):
        self.traffic_cascade = cv2.CascadeClassifier(cascade_classifier)
        self.lights_in_queue = [QUEUE_SIZE, 0, 0, 0]
        self.queue = []
        for i in range(QUEUE_SIZE):
            self.queue.append(UNKNOWN)

    def detect(self, image):
        """
        Detect a traffic light from the image(BGR image).
        """
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        traffic_light = self.traffic_cascade.detectMultiScale(gray, minNeighbors=5, minSize=(30, 30))

        cnt = [0, 0, 0, 0]
        for (x_pos, y_pos, width, height) in traffic_light:
            color_id = self.classify_light(image[y_pos:y_pos+height, x_pos:x_pos+width])
            cv2.putText(image, 'Traffic Light: ' + COLORS_NAME[color_id], (x_pos-5, y_pos-5), cv2.FONT_HERSHEY_SIMPLEX, 0.5, COLORS[color_id], 2)
            cv2.rectangle(image, (x_pos, y_pos), (x_pos+width, y_pos+height), COLORS[color_id], 2)
            cnt[color_id] += 1

        traffic_color = argmax(cnt)
        self.queue.append(traffic_color)
        self.lights_in_queue[traffic_color] += 1
        self.lights_in_queue[self.queue.pop(0)] -= 1

        if self.lights_in_queue[RED] >= 1:
            return "red"
        if self.lights_in_queue[YELLOW] >= 3:
            return "yellow"
        if self.lights_in_queue[GREEN] >= 5:
            return "green"
        return "unknown"

    def classify_light(self, image):
        hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

        mask = cv2.inRange(hsv, RED_MIN, RED_MAX)
        red_cnt = cv2.countNonZero(mask)

        mask = cv2.inRange(hsv, YELLOW_MIN, YELLOW_MAX)
        yellow_cnt = cv2.countNonZero(mask)

        mask = cv2.inRange(hsv, GREEN_MIN, GREEN_MAX)
        green_cnt = cv2.countNonZero(mask)

        if red_cnt > yellow_cnt and red_cnt > green_cnt:
            return RED
        if yellow_cnt > red_cnt and yellow_cnt > green_cnt:
            return YELLOW
        if green_cnt > red_cnt and green_cnt > yellow_cnt:
            return GREEN
        return UNKNOWN


if __name__ == '__main__':
    detector = TrafficLightDetector()
    cap = cv2.VideoCapture("nvcamerasrc ! video/x-raw(memory:NVMM), width=(int)%d, height=(int)%d,format=(string)I420, framerate=(fraction)30/1 ! nvvidconv flip-method=0 ! video/x-raw, format=(string)BGRx ! videoconvert ! video/x-raw, format=(string)BGR ! appsink" % (640, 320))
    while cv2.waitKey(10) != ord('q'):
        ret, frame = cap.read()
        color = detector.detect(frame)
        cv2.imshow('frame', frame)
        print(color)

    cv2.destroyAllWindows()
    cap.release()
