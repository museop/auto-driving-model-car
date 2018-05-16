import cv2
import time
from Camera.camera import Camera, load_calibration, undistort
from ObjectDetection.traffic_light_detection import TrafficLightDetector
from ObjectDetection.stop_sign_detection import StopSignDetector

camera = Camera()
detector = TrafficLightDetector('cascade.xml')
#  detector = StopSignDetector('./stop_sign.xml')
mtx, dist = load_calibration('./Camera/mtx.txt', './Camera/dist.txt')

i = 0
while camera.is_opened():
    start_time = time.time()
    frame = camera.capture()
    frame = undistort(frame, mtx, dist)
    ret = detector.detect(frame)
    print(ret)

    #  height, width = frame.shape[:2]
    #  frame = cv2.resize(frame, None, fx=2, fy=2, interpolation=cv2.INTER_CUBIC)

    cv2.imshow('frame', frame)

    key = cv2.waitKey(10) & 0xFF
    if key == ord('q'):
        break
    if key == ord('s'):
        cv2.imwrite(str(i) + '.jpg', frame)
    i += 1

cv2.destroyAllWindows()
