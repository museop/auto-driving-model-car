import cv2
import scipy.misc

f = open('data/data.txt', 'r')

for line in f:
    image = cv2.imread('data/' + line.split()[0])
    angle = float(line.split()[1])

    #  cv2.imshow('image', image[-100:])
    #  print(angle)
    #  if (cv2.waitKey(10) & 0xFF == ord('q')):
        #  cv2.destroyAllWindows()
        #  break



