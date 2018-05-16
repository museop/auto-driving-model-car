import os
import cv2
import glob2
import numpy as np


DEFAULT_MTX_FILE_PATH = os.path.join(os.path.dirname(__file__), "mtx.txt")
DEFAULT_DIST_FILE_PATH = os.path.join(os.path.dirname(__file__), "dist.txt")

class CameraError(Exception):
    pass


def camera_calibration(directory, filename, nx, ny):
    objp = np.zeros((nx*ny,3), np.float32)
    objp[:,:2] = np.mgrid[0:nx, 0:ny].T.reshape(-1,2)

    objpoints = []
    imgpoints = []

    images = glob2.glob('./'+directory+'/'+filename+'*.jpg')

    for idx, fname in enumerate(images):
        img = cv2.imread(fname)
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        ret, corners = cv2.findChessboardCorners(gray, (nx,ny), None)

        if ret == True:
            objpoints.append(objp)
            imgpoints.append(corners)

            #visualize
            img = cv2.drawChessboardCorners(img, (nx,ny), corners, ret)
            cv2.imshow('input image', img)
            cv2.waitKey(200)
    cv2.destroyAllWindows()

    if (len(objpoints) == 0 or len(imgpoints) == 0):
        raise CameraError("Calibration Failed")

    img_size = (img.shape[1], img.shape[0])
    ret, mtx, dist, rvecs, tvecs = cv2.calibrateCamera(objpoints, imgpoints, img_size, None, None)

    return mtx, dist


def undistort(image, mtx, dist):
    image = cv2.undistort(image, mtx, dist, None, mtx)
    return image


def save_calibration(directory, prefix):
    mtx, dist = camera_calibration(directory, prefix, 10, 7)
    np.savetxt(DEFAULT_MTX_FILE_PATH, mtx, delimiter=',')
    np.savetxt(DEFAULT_DIST_FILE_PATH, dist, delimiter=',')


def load_calibration(mtx_file=DEFAULT_MTX_FILE_PATH, dist_file=DEFAULT_DIST_FILE_PATH):
    mtx = np.loadtxt(mtx_file, delimiter=',')
    dist = np.loadtxt(dist_file, delimiter=',')
    return mtx, dist

