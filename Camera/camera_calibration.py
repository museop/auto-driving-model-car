import cv2
import glob2
import numpy as np

class Error(Exception):
    pass


def camera_calibration(directory, filename, nx, ny):
    objp = np.zeros((nx*ny,3), np.float32)
    objp[:,:2] = np.mgrid[0:nx, 0:ny].T.reshape(-1, 2)

    objpoints = []
    imgpoints = []

    images = glob2.glob('./' + directory + '/' + filename + '*.jpg')

    for idx, fname in enumerate(images):
        img = cv2.imread(fname)
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        ret, corners = cv2.findChessboardCorners(gray, (nx, ny), None)

        if ret == True:
            objpoints.append(objp)
            imgpoints.append(corners)

            img = cv2.drawChessboardCorners(img, (nx, ny), corners, ret)
            cv2.imshow('input image', img)
            cv2.waitKey(500)
    cv2.destroyAllWindows()

    if (len(objpoints) == 0 or len(imgpoints) == 0):
        raise Error("Calibration Failed")

    img_size = (img.shape[1], img.shape[0])
    ret, mtx, dist, rvecs, tvecs = cv2.calibrateCamera(objpoints, imgpoints, img_size, None, None)

    return mtx, dist


def undistort(image, mtx, dist):
    image = cv2.undistort(image, mtx, dist, None, mtx)
    return image


mtx, dist = camera_calibration('camera_cal', 'calibration', 10, 7)
np.savetxt('mtx.txt', mtx, delimiter=',')
np.savetxt('dist.txt', dist, delimiter=',')
