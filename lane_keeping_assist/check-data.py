import cv2
import scipy.misc

f = open('data/data.txt', 'r')

for line in f:
    image = cv2.imread('data/' + line.split()[0])
    angle = float(line.split()[1])
    #  image= cv2.resize(image,None, fx=2, fy=2, interpolation=cv2.INTER_CUBIC)
    #  cv2.imshow('image', image)
    #  print(angle)
    #  if (cv2.waitKey(30) & 0xFF == ord('q')):
        #  cv2.destroyAllWindows()
        #  break



