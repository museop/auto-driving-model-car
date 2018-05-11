import cv2

QUEUE_SIZE = 20
THRESHHOLD = 1

class StopSignDetector(object):
    def __init__(self, cascade_classifier='Stopsign_HAAR.xml'):
        self.font = cv2.FONT_HERSHEY_SIMPLEX
        self.stopsign_cascade = cv2.CascadeClassifier(cascade_classifier)
        self.queue = []
        self.num_true_in_queue = 0
        for i in range(QUEUE_SIZE):
            self.queue.append(False)

    def detect(self, image):
        """
        Detect stop signs from the image(BGR image).
        """
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        stop_signs = self.stopsign_cascade.detectMultiScale(gray, minNeighbors=5, minSize=(30, 30))

        for (x_pos, y_pos, width, height) in stop_signs:
            cv2.putText(image, 'Detected Stop Sign', (x_pos-5, y_pos-5), self.font, 0.2, (0, 255, 0), 2)
            cv2.rectangle(image, (x_pos, y_pos), (x_pos+width, y_pos+height), (0, 0, 255), 2)

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

        

if __name__ == '__main__':
    detector = StopSignDetector()
    cap_width, cap_height = 640, 320
    cap = cv2.VideoCapture("nvcamerasrc ! video/x-raw(memory:NVMM), width=(int)%d, height=(int)%d,format=(string)I420, framerate=(fraction)30/1 ! nvvidconv flip-method=0 ! video/x-raw, format=(string)BGRx ! videoconvert ! video/x-raw, format=(string)BGR ! appsink" % (cap_width, cap_height))
    while cv2.waitKey(10) != ord('q'):
        ret, frame = cap.read()
        res = detector.detect(frame)
        print(res)
        cv2.imshow('frame', frame)
    cv2.destroyAllWindows()
    cap.release()
        
