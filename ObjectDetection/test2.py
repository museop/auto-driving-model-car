import cv2
import numpy as np

def red_green_yellow(bgr_image):
    rows, cols = bgr_image.shape[:2]
    hsv = cv2.cvtColor(bgr_image, cv2.COLOR_BGR2HSV)
    sum_saturation = np.sum(hsv[:,:,1]) # sum the brightness values
    area = rows * cols
    avg_saturation = sum_saturation / area

    sat_low = int(avg_saturation * 1.3)
    val_low = 140

    # Green
    lower_green = np.array([70, sat_low, val_low])
    upper_green = np.array([100, 255, 255])
    green_mask = cv2.inRange(hsv, lower_green, upper_green)
    #  green_result = cv2.bitwise_and(bgr_image, bgr_image, mask=green_mask)
    sum_green = cv2.countNonZero(green_mask)

    # Yellow
    lower_yellow = np.array([10, sat_low, val_low])
    upper_yellow = np.array([60, 255, 255])
    yellow_mask = cv2.inRange(hsv, lower_yellow, upper_yellow)
    #  yellow_result = cv2.bitwise_and(bgr_image, bgr_image, mask=yellow_mask)
    sum_yellow = cv2.countNonZero(yellow_mask)

    # Red
    lower_red = np.array([150, sat_low, val_low])
    upper_red = np.array([180, 255, 255])
    red_mask = cv2.inRange(hsv, lower_red, upper_red)
    #  red_result = cv2.bitwise_and(bgr_image, bgr_image, mask=red_mask)
    sum_red = cv2.countNonZero(red_mask)

    if sum_red >= sum_yellow and sum_red >= sum_green:
        return 0
    if sum_yellow >= sum_green:
        return 1
    return 2

if __name__ == '__main__':
    cap = cv2.VideoCapture("nvcamerasrc ! video/x-raw(memory:NVMM), width=(int)640, height=(int)320,format=(string)I420, framerate=(fraction)30/1 ! nvvidconv flip-method=0 ! video/x-raw, format=(string)BGRx ! videoconvert ! video/x-raw, format=(string)BGR ! appsink")


    traffic_lights = ["red", "yellow", "green"]

    while cv2.waitKey(25) != ord('q'):
        ret, frame = cap.read()
        cv2.imshow('frame', frame)

        lights = red_green_yellow(frame)

        print(traffic_lights[lights])
    cv2.destroyAllWindows() 
        


        
