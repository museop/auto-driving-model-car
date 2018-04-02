import cv2

class Camera(object):
    
    def __init__(self):
        self.cap = 0
        self.cap = cv2.VideoCapture("nvcamerasrc ! video/x-raw(memory:NVMM), width=(int)1280, height=(int)720,format=(string)I420, framerate=(fraction)30/1 ! nvvidconv flip-method=0 ! video/x-raw, format=(string)BGRx ! videoconvert ! video/x-raw, format=(string)BGR ! appsink")
        if self.cap.isOpened() == False:
            print("Failed to open camera.")

    def frame(self):
        ret, frm = self.cap.read()
        return frm

    def show_camera(self):
        print("Press 'q' if you want to close")
        while self.cap.isOpened():
            frm = self.frame()
            cv2.imshow("frame", frm)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        cv2.destroyAllWindows()

    def __del__(self):
        self.cap.release()


if __name__ == "__main__":
    camera = Camera()
    camera.show_camera()

