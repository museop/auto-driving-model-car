import os
import sys
import cv2


if __name__ == '__main__':
    sys.path.insert(0, os.path.abspath('..'))
    from camera.jetson_tx2_camera import LI_IMX377_MIPI_M12
    from traffic_signal_detector.traffic_signal_detector import TrafficSignalDetector

    camera = LI_IMX377_MIPI_M12()
    traffic_signal_detector = TrafficSignalDetector()

    while camera.is_opened():
        frame = camera.capture_frame()
        frame = camera.calibrate(frame)
        can_go = traffic_signal_detector.can_go_forward(frame)
        print(can_go)
        cv2.imshow('frame', frame)
        #  stop_signs = traffic_signal_detector.detect_stop_signs(frame)
        #  traffic_lights = traffic_signal_detector.detect_traffic_lights(frame)
        #  cv2.imshow('stop_signs', stop_signs)
        #  cv2.imshow('traffic_lights', traffic_lights)

        key = cv2.waitKey(10) & 0xFF
        if key == ord('q'):
            cv2.destroyAllWindows()
            break

