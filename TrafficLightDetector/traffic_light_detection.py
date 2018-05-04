import cv2

class TrafficLightDetector(object):
    def __init__(self, cascade_classifier='TrafficLight_HAAR.xml'):
        self.traffic_cascade = cv2.CascadeClassifier(cascade_classifier)
        self.red_light = False
        self.green_light = False
        self.yellow_light = False

    def detect(self, image, image_type='rgb'):
        if image_type == 'rgb':
            gray = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
        elif image_type == 'bgr':
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        
        traffic_light = self.traffic_cascade.detectMultiScale(gray)
        for (x_pos, y_pos, width, height) in traffic_light:
            #self.classify_light(image, x_pos, y_pos, width, height)
            image = cv2.rectangle(image, (x_pos, y_pos), (x_pos + width, y_pos + height), (255, 0, 0), 2)
        

