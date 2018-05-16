import cv2
from camera import Camera
from calibration import undistort
from calibration import load_calibration


CAMERA_WIDTH, CAMERA_HEIGHT = 320, 160


class JetsonTX2Camera(Camera):
    def __init__(self):
        self.width = CAMERA_WIDTH
        self.height = CAMERA_HEIGHT
        self.cap = None
        self.mtx, self.dist = load_calibration()
        self.open()

    def open(self):
        self.cap = cv2.VideoCapture("nvcamerasrc ! video/x-raw(memory:NVMM), width=(int)%d, height=(int)%d,format=(string)I420, framerate=(fraction)30/1 ! nvvidconv flip-method=0 ! video/x-raw, format=(string)BGRx ! videoconvert ! video/x-raw, format=(string)BGR ! appsink" % (CAMERA_WIDTH, CAMERA_HEIGHT))

        if self.is_opened() == False:
            print("Failed to open camera.")
    
    def is_opened(self):
        return self.cap.isOpened()

    def capture_frame(self):
        ret, frame = self.cap.read()
        if ret == False:
            print("Failed to capture frame.")
        return frame

    def calibrate(self, frame):
        return undistort(frame, self.mtx, self.dist)

    def show_frames(self):
        print("Press 'q' if you want to close")
        while self.cap.isOpened():
            frame = self.capture_frame()
            frame = self.calibrate(frame)
            cv2.imshow('frame', frame)
            if cv2.waitKey(10) & 0xFF == ord('q'):
                break
        cv2.destroyAllWindows()
    
    def save_frame(self, directory, filename, frame):
        path_to_save = directory + '/' + filename
        cv2.imwrite(path_to_save, frame)

    def __del__(self):
        self.cap.release()

