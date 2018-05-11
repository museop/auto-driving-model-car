import cv2
from Camera.camera import Camera, load_calibration, undistort
from ObjectDetection.traffic_light_detection import TrafficLightDetector
from ObjectDetection.stop_sign_detection import StopSignDetector

camera = Camera()
detector = TrafficLightDetector('./ObjectDetection/TrafficLight_HAAR.xml')
#  detector = StopSignDetector('./ObjectDetection/Stopsign_HAAR.xml')
mtx, dist = load_calibration('./Camera/mtx.txt', './Camera/dist.txt')

while camera.is_opened():
    frame = camera.capture()
    frame = undistort(frame, mtx, dist)
    ret = detector.detect(frame)
    print(ret)

    #  height, width = frame.shape[:2]
    #  frame = cv2.resize(frame, (width*4, height*4), interpolation=cv2.INTER_CUBIC)
    cv2.imshow('frame', frame)

    if cv2.waitKey(10) & 0xFF == ord('q'):
        break

cv2.destroyAllWindows()
