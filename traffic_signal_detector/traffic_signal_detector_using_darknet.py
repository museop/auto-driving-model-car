from ctypes import *
import numpy as np
import os
import math
import random
import scipy.misc
import cv2
import time

def sample(probs):
    s = sum(probs)
    probs = [a/s for a in probs]
    r = random.uniform(0, 1)
    for i in range(len(probs)):
        r = r - probs[i]
        if r <= 0:
            return i
    return len(probs)-1

def c_array(ctype, values):
    arr = (ctype*len(values))()
    arr[:] = values
    return arr

class BOX(Structure):
    _fields_ = [("x", c_float),
                ("y", c_float),
                ("w", c_float),
                ("h", c_float)]

class DETECTION(Structure):
    _fields_ = [("bbox", BOX),
                ("classes", c_int),
                ("prob", POINTER(c_float)),
                ("mask", POINTER(c_float)),
                ("objectness", c_float),
                ("sort_class", c_int)]


class IMAGE(Structure):
    _fields_ = [("w", c_int),
                ("h", c_int),
                ("c", c_int),
                ("data", POINTER(c_float))]

class METADATA(Structure):
    _fields_ = [("classes", c_int),
                ("names", POINTER(c_char_p))]

    

DEFAULT_DARKNET_LIB_PATH = os.path.join(os.path.dirname(__file__), "resources", "libdarknet.so")

lib = CDLL(DEFAULT_DARKNET_LIB_PATH, RTLD_GLOBAL)
lib.network_width.argtypes = [c_void_p]
lib.network_width.restype = c_int
lib.network_height.argtypes = [c_void_p]
lib.network_height.restype = c_int

predict = lib.network_predict
predict.argtypes = [c_void_p, POINTER(c_float)]
predict.restype = POINTER(c_float)

set_gpu = lib.cuda_set_device
set_gpu.argtypes = [c_int]

make_image = lib.make_image
make_image.argtypes = [c_int, c_int, c_int]
make_image.restype = IMAGE

get_network_boxes = lib.get_network_boxes
get_network_boxes.argtypes = [c_void_p, c_int, c_int, c_float, c_float, POINTER(c_int), c_int, POINTER(c_int)]
get_network_boxes.restype = POINTER(DETECTION)

make_network_boxes = lib.make_network_boxes
make_network_boxes.argtypes = [c_void_p]
make_network_boxes.restype = POINTER(DETECTION)

free_detections = lib.free_detections
free_detections.argtypes = [POINTER(DETECTION), c_int]

free_ptrs = lib.free_ptrs
free_ptrs.argtypes = [POINTER(c_void_p), c_int]

network_predict = lib.network_predict
network_predict.argtypes = [c_void_p, POINTER(c_float)]

reset_rnn = lib.reset_rnn
reset_rnn.argtypes = [c_void_p]

load_net = lib.load_network
load_net.argtypes = [c_char_p, c_char_p, c_int]
load_net.restype = c_void_p

do_nms_obj = lib.do_nms_obj
do_nms_obj.argtypes = [POINTER(DETECTION), c_int, c_int, c_float]

do_nms_sort = lib.do_nms_sort
do_nms_sort.argtypes = [POINTER(DETECTION), c_int, c_int, c_float]

free_image = lib.free_image
free_image.argtypes = [IMAGE]

letterbox_image = lib.letterbox_image
letterbox_image.argtypes = [IMAGE, c_int, c_int]
letterbox_image.restype = IMAGE

load_meta = lib.get_metadata
lib.get_metadata.argtypes = [c_char_p]
lib.get_metadata.restype = METADATA

load_image = lib.load_image_color
load_image.argtypes = [c_char_p, c_int, c_int]
load_image.restype = IMAGE

rgbgr_image = lib.rgbgr_image
rgbgr_image.argtypes = [IMAGE]

predict_image = lib.network_predict_image
predict_image.argtypes = [c_void_p, IMAGE]
predict_image.restype = POINTER(c_float)

ndarray_image = lib.ndarray_to_image
ndarray_image.argtypes = [POINTER(c_ubyte), POINTER(c_long), POINTER(c_long)]
ndarray_image.restype = IMAGE

def classify(net, meta, im):
    out = predict_image(net, im)
    res = []
    for i in range(meta.classes):
        res.append((meta.names[i], out[i]))
    res = sorted(res, key=lambda x: -x[1])
    return res

def detect(net, meta, image, thresh=.5, hier_thresh=.5, nms=.45):
    im = load_image(image, 0, 0)
    num = c_int(0)
    pnum = pointer(num)
    predict_image(net, im)
    dets = get_network_boxes(net, im.w, im.h, thresh, hier_thresh, None, 0, pnum)
    num = pnum[0]
    if (nms): do_nms_obj(dets, num, meta.classes, nms);

    res = []
    for j in range(num):
        for i in range(meta.classes):
            if dets[j].prob[i] > 0:
                b = dets[j].bbox
                res.append((meta.names[i], dets[j].prob[i], (b.x, b.y, b.w, b.h)))
    res = sorted(res, key=lambda x: -x[1])
    free_image(im)
    free_detections(dets, num)
    return res

def nparray_to_image(img):
    data = img.ctypes.data_as(POINTER(c_ubyte))
    image = ndarray_image(data, img.ctypes.shape, img.ctypes.strides)

    return image


DEFAULT_CFG_PATH = os.path.join(os.path.dirname(__file__), "resources", "yolov3-tiny-myobj.cfg")
DEFAULT_WEIGHTS__PATH = os.path.join(os.path.dirname(__file__), "resources", "yolov3-tiny-myobj.weights")
DEFAULT_META_DATA_PATH = os.path.join(os.path.dirname(__file__), "resources", "obj.data")

QUEUE_SIZE = 5
THRESHHOLD = 1


class TrafficSignalDetectorUsingDarknet(object):
    """docstring for TrafficSignalDetectorUsingDarknet"""
    def __init__(self):
        super(TrafficSignalDetectorUsingDarknet, self).__init__()
        print('init TrafficSignalDetectorUsingDarknet')
        self.net = load_net(DEFAULT_CFG_PATH, DEFAULT_WEIGHTS__PATH, 0) 
        self.meta = load_meta(DEFAULT_META_DATA_PATH)
        self.thresh = .5
        self.hier_thresh = .5
        self.nms = .45
        self.queue = []
        self.num_true_in_queue = 0
        for i in range(QUEUE_SIZE):
            self.queue.append(False)

    def detect(self, frame):
        im = nparray_to_image(frame)
        num = c_int(0)
        pnum = pointer(num)
        predict_image(self.net, im)
        dets = get_network_boxes(self.net, im.w, im.h, self.thresh, self.hier_thresh, None, 0, pnum)
        num = pnum[0]
        if (self.nms): do_nms_obj(dets, num, self.meta.classes, self.nms);

        res = []
        for j in range(num):
            for i in range(self.meta.classes):
                if dets[j].prob[i] > 0:
                    b = dets[j].bbox
                    res.append((self.meta.names[i], dets[j].prob[i], (b.x, b.y, b.w, b.h)))
        res = sorted(res, key=lambda x: -x[1])
        free_image(im)
        free_detections(dets, num)
        return res
    
    def can_go_forward(self, frame, low_accuracy):
        detected_objs = self.detect(frame)
        num_objs = len(detected_objs)
        
        flag = False
        for i in range(num_objs):
            label, acc, (x, y, width, height) = detected_objs[i]
            
            if label == 'green traffic light':
                continue
                
            if acc > low_accuracy:
                flag = True
        
        if flag == True:
            x = self.queue.pop(0)
            if x == False:
                self.num_true_in_queue += 1
            self.queue.append(True)
        else:
            x = self.queue.pop(0)
            if x == True:
                self.num_true_in_queue -= 1
            self.queue.append(False)

        return self.num_true_in_queue < THRESHHOLD

    def visualize_traffic_info(self, frame):
        detected_objs = self.detect(frame)
        num_objs = len(detected_objs)

        for i in range(num_objs):
            label, acc, (x, y, width, height) = detected_objs[i]
            x1 = int(x-width/2)
            y1 = int(y-height/2)
            x2 = int(x+width/2)
            y2 = int(y+height/2)
            cv2.putText(frame, label+'(%.2f)'%acc, (x1-5, y1-5), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255))
            cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 0, 255), 2)
        return frame

    def avg_processing_time(self, frame_height, frame_width):
        img = np.ones((frame_height,frame_width,3), np.uint8) * 255
        self.detect(img) # The initial detecting time is excluded.

        h, w = img.shape[:2]

        colors = [(255, 0, 0), (0, 255, 0), (0, 0, 255), (0, 0, 0), (255, 255, 255)]
        num_iterations = len(colors)

        sum_time = 0.0
        for i in range(num_iterations):
            for y in range(h):
                for x in range(w):
                    img[y][x] = colors[i]
            start_time = time.time()
            self.detect(img)
            sum_time = sum_time + (time.time() - start_time)

        avg_time = sum_time/num_iterations
        return avg_time

    def __del__(self):
        print('delete TrafficSignalDetectorUsingDarknet')
        

if __name__ == "__main__":
    cap = cv2.VideoCapture("nvcamerasrc ! video/x-raw(memory:NVMM), width=(int)%d, height=(int)%d,format=(string)I420, framerate=(fraction)30/1 ! nvvidconv flip-method=0 ! video/x-raw, format=(string)BGRx ! videoconvert ! video/x-raw, format=(string)BGR ! appsink"%(320, 160))

    detector = TrafficSignalDetectorUsingDarknet()

    while cap.isOpened():
        ret, frame = cap.read()
        frame = detector.visualize_traffic_info(frame)
        cv2.imshow('frame', frame)
        key = cv2.waitKey(1) & 0xff
        if key == ord('q'):
            break
        elif key == ord('s'):
            cv2.imwrite('image.jpg', frame)

    cv2.destroyAllWindows()
