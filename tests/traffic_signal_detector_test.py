import os
import sys
import cv2


if __name__ == '__main__':
    sys.path.insert(0, os.path.abspath('..'))
    from camera.jetson_tx2_camera import LI_IMX377_MIPI_M12
    from traffic_signal_detector.traffic_signal_detector_using_darknet import TrafficSignalDetectorUsingDarknet

    camera = LI_IMX377_MIPI_M12()
    traffic_signal_detector = TrafficSignalDetectorUsingDarknet()

    while camera.is_opened():
        frame = camera.capture_frame()

        frame = traffic_signal_detector.visualize_traffic_info(frame)
        cv2.imshow('frame', frame)

        key = cv2.waitKey(30) & 0xFF
        if key == ord('q'):
            break

    cv2.destroyAllWindows()

