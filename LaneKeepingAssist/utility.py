import cv2
import numpy as np
import scipy.misc
import os
from sklearn.model_selection import train_test_split

MIN_PWM_VALUE, MAX_PWM_VALUE, MIN_DEGREE, MAX_DEGREE = 234.0, 380.0, -40.0, 40.0

IMAGE_HEIGHT, IMAGE_WIDTH, IMAGE_CHANNELS = 66, 200, 3
INPUT_SHAPE = (IMAGE_HEIGHT, IMAGE_WIDTH, IMAGE_CHANNELS)


def range_map(x, in_min, in_max, out_min, out_max):
    """
    Re-maps a number from one range to another.
    """
    return (x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min


def degree2radian(degree):
    """
    Converts degree to radian
    """
    return degree * scipy.pi / 180.0


def radian2degree(radian):
    """
    Converts radian to degree
    """
    return radian * 180.0 / scipy.pi


def pwm_value2steering_angle(pwm_value):
    """
    Converts pwm value to steering angle(radian).
    """
    steers_deg = range_map(pwm_value, MIN_PWM_VALUE, MAX_PWM_VALUE, MIN_DEGREE, MAX_DEGREE)
    return degree2radian(steers_deg)


def steering_angle2pwm_value(steering_angle):
    """
    Converts steering angle(radian) to pwm value.
    """
    steers_deg = radian2degree(steers)
    return range_map(steers_deg, MIN_DEGREE, MAX_DEGREE, MIN_PWM_VALUE, MAX_PWM_VALUE)



def load_image(data_dir, image_file):
    """
    Load RGB images from a file
    """
    return scipy.misc.imread(os.path.join(data_dir, image_file.strip()))


def reshape(image):
    """
    Reshape the image to the input shape used by the network model
    """
    return scipy.misc.imresize(image[-100:], [IMAGE_HEIGHT, IMAGE_WIDTH])


def rgb2yuv(image):
    """
    Convert the image from RGB to YUV (This is what the NVIDIA model does)
    """
    return cv2.cvtColor(image, cv2.COLOR_RGB2YUV)


def bgr2yuv(image):
    """
    Convert the image from BGR to YUV (This is what the NVIDIA model does)
    """
    return cv2.cvtColor(image, cv2.COLOR_BGR2YUV)


def preprocess(image):
    """
    Combine all preprocess functions into one
    """
    image = reshape(image)
    image = rgb2yuv(image)
    return image


def preprocess2(image):
    """
    """
    image = reshape(image)
    image = bgr2yuv(image)
    return image


def random_flip(image, steering_angle):
    """
    Randomly flipt the image left <-> right, and adjust the steering angle.
    """
    if np.random.rand() < 0.5:
        image = cv2.flip(image, 1)
        steering_angle = -steering_angle
    return image, steering_angle


def random_translate(image, steering_angle, range_x, range_y):
    """
    Randomly shift the image virtially and horizontally (translation).
    """
    trans_x = range_x * (np.random.rand() - 0.5)
    trans_y = range_y * (np.random.rand() - 0.5)
    steering_angle += trans_x * 0.002
    trans_m = np.float32([[1, 0, trans_x], [0, 1, trans_y]])
    height, width = image.shape[:2]
    image = cv2.warpAffine(image, trans_m, (width, height))
    return image, steering_angle


def random_brightness(image):
    """
    Randomly adjust brightness of the image.
    """
    # HSV (Hue, Saturation, Value) is also called HSB ('B' for Brightness).
    hsv = cv2.cvtColor(image, cv2.COLOR_RGB2HSV)
    ratio = 1.0 + 0.4 * (np.random.rand() - 0.5)
    hsv[:,:,2] =  hsv[:,:,2] * ratio
    return cv2.cvtColor(hsv, cv2.COLOR_HSV2RGB)


def augument(data_dir, image_file, steering_angle, range_x=100, range_y=10):
    """
    Generate an augumented image and adjust steering angle.
    (The steering angle is associated with the center image)
    """
    image = load_image(data_dir, image_file)
    image, steering_angle = random_flip(image, steering_angle)
    image, steering_angle = random_translate(image, steering_angle, range_x, range_y)
    image = random_brightness(image)
    return image, steering_angle


def batch_generator(data_dir, image_paths, steering_angles, batch_size, is_training):
    """
    Generate training image give image paths and associated steering angles
    """
    images = np.empty([batch_size, IMAGE_HEIGHT, IMAGE_WIDTH, IMAGE_CHANNELS])
    steers = np.empty(batch_size)
    while True:
        i = 0
        for index in np.random.permutation(len(image_paths)):
            image_path = image_paths[index]
            steering_angle = steering_angles[index]
            # argumentation
            if is_training and np.random.rand() < 0.6:
                image, steering_angle = augument(data_dir, image_path, steering_angle)
            else:
                image = load_image(data_dir, image_path) 
            # add the image and steering angle to the batch
            images[i] = preprocess(image)
            steers[i] = steering_angle
            i += 1
            if i == batch_size:
                break
        yield images, steers


def load_data(data_dir, test_size):
    """
    Load training data and split it into training and validation set
    """
    xs = []
    ys = []
    with open(os.path.join(data_dir, 'data.txt')) as f:
        for line in f:
            xs.append(line.split()[0])
            ys.append(pwm_value2steering_angle(float(line.split()[1])))

    x_train, x_valid, y_train, y_valid = train_test_split(xs, ys, test_size=test_size, random_state=0)

    return x_train, x_valid, y_train, y_valid
    

