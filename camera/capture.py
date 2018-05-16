import cv2
import camera

cap = cv2.VideoCapture("nvcamerasrc ! video/x-raw(memory:NVMM), width=(int)320, height=(int)160,format=(string)I420, framerate=(fraction)30/1 ! nvvidconv flip-method=0 ! video/x-raw, format=(string)BGRx ! videoconvert ! video/x-raw, format=(string)BGR ! appsink")

i = 0
mtx, dist = camera.load_calibration()

while cap.isOpened():
    ret, frame = cap.read()
    frame = camera.undistort(frame, mtx, dist)
    frame = cv2.resize(frame, None, fx=2, fy=2, interpolation=cv2.INTER_CUBIC)
    cv2.imshow('frame', frame)
    key = cv2.waitKey(10) & 0xFF

    if key == ord('q'):
        break

    elif key == ord('s'):
        cv2.imwrite(str(i) + '.jpg', frame)
        i += 1

cv2.destroyAllWindows()
cap.release()
