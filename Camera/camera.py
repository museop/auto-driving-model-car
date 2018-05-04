import cv2

class Camera(object):
    def __init__(self, width=640, height=360):
        self.cap = cv2.VideoCapture("nvcamerasrc ! video/x-raw(memory:NVMM), width=(int)%d, height=(int)%d,format=(string)I420, framerate=(fraction)30/1 ! nvvidconv flip-method=0 ! video/x-raw, format=(string)BGRx ! videoconvert ! video/x-raw, format=(string)BGR ! appsink" % (width, height))

        if self.cap.isOpened() == False:
            print("Failed to open camera.")


    def capture(self):
        ret, frame = self.cap.read()
        return frame


    def show_frames(self):
        print("Press 'q' if you want to close")
        while self.cap.isOpened():
            frame = self.capture()
            cv2.imshow("frame", frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        cv2.destroyAllWindows()


    def __del__(self):
        self.cap.release()


if __name__ == "__main__":
    camera = Camera(1280, 640)
    camera.show_frames()

