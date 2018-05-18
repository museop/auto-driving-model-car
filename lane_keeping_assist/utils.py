import cv2
import numpy as np
import scipy.misc
import random
import os
from sklearn.model_selection import train_test_split


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


def random_shadow(image):
    """
    Generates and adds random shadow
    """
    top_y = 320*np.random.uniform()
    top_x = 0
    bot_x = 160
    bot_y = 320*np.random.uniform()
    image_hls = cv2.cvtColor(image,cv2.COLOR_RGB2HLS)
    shadow_mask = 0*image_hls[:,:,1]
    X_m = np.mgrid[0:image.shape[0],0:image.shape[1]][0]
    Y_m = np.mgrid[0:image.shape[0],0:image.shape[1]][1]
    shadow_mask[((X_m-top_x)*(bot_y-top_y) -(bot_x - top_x)*(Y_m-top_y) >=0)]=1
    #random_bright = .25+.7*np.random.uniform()
    if np.random.randint(2)==1:
        random_bright = .5
        cond1 = shadow_mask==1
        cond0 = shadow_mask==0
        if np.random.randint(2)==1:
            image_hls[:,:,1][cond1] = image_hls[:,:,1][cond1]*random_bright
        else:
            image_hls[:,:,1][cond0] = image_hls[:,:,1][cond0]*random_bright    
    image = cv2.cvtColor(image_hls,cv2.COLOR_HLS2RGB)
    return image


def random_snow(image):
    """
    Randomly make snow in the image.
    """
    if np.random.rand() < 0.2:
        image_HLS = cv2.cvtColor(image,cv2.COLOR_RGB2HLS) ## Conversion to HLS
        image_HLS = np.array(image_HLS, dtype = np.float64) 
        brightness_coefficient = 2.5 
        snow_point=random.randint(80, 100)
        image_HLS[:,:,1][image_HLS[:,:,1]<snow_point] = image_HLS[:,:,1][image_HLS[:,:,1]<snow_point]*brightness_coefficient ## scale pixel values up for channel 1(Lightness)
        image_HLS[:,:,1][image_HLS[:,:,1]>255]  = 255 ##Sets all values above 255 to 255
        image_HLS = np.array(image_HLS, dtype = np.uint8)
        image_RGB = cv2.cvtColor(image_HLS,cv2.COLOR_HLS2RGB) ## Conversion to RGB
        return image_RGB
    else:
        return image


def generate_random_lines(imshape,slant,drop_length):
    """
    Generate lines.
    """
    drops=[]
    heavy = random.randint(100, 300)
    for _ in range(heavy): ## If You want heavy rain, try increasing this
        if slant<0:
            x= np.random.randint(slant,imshape[1])
        else:
            x= np.random.randint(0,imshape[1]-slant)
        y= np.random.randint(0,imshape[0]-drop_length)
        drops.append((x,y))
    return drops
        
    
def random_rain(image):
    """
    Randomly make rain in the image.
    """
    if np.random.rand() < 0.2:
        imshape = image.shape
        slant_extreme=10
        slant= np.random.randint(-slant_extreme,slant_extreme) 
        drop_length=1
        drop_width=1
        drop_color=(200,200,200) ## a shade of gray
        rain_drops= generate_random_lines(imshape,slant,drop_length)
        
        for rain_drop in rain_drops:
            cv2.line(image,(rain_drop[0],rain_drop[1]),(rain_drop[0]+slant,rain_drop[1]+drop_length),drop_color,drop_width)
        image= cv2.blur(image,(3,3)) ## rainy view are blurry
        
        brightness_coefficient = 0.7 ## rainy days are usually shady 
        image_HLS = cv2.cvtColor(image,cv2.COLOR_RGB2HLS) ## Conversion to HLS
        image_HLS[:,:,1] = image_HLS[:,:,1]*brightness_coefficient ## scale pixel values down for channel 1(Lightness)
        image_RGB = cv2.cvtColor(image_HLS,cv2.COLOR_HLS2RGB) ## Conversion to RGB
        return image_RGB
    else:
        return image


def augument(data_dir, image_file, steering_angle, range_x=100, range_y=10):
    """
    Generate an augumented image and adjust steering angle.
    (The steering angle is associated with the center image)
    """
    image = load_image(data_dir, image_file)
    image, steering_angle = random_flip(image, steering_angle)
    image, steering_angle = random_translate(image, steering_angle, range_x, range_y)
    image = random_snow(image)
    image = random_rain(image)
    image = random_shadow(image)
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
            ys.append(float(line.split()[1]))

    x_train, x_valid, y_train, y_valid = train_test_split(xs, ys, test_size=test_size, random_state=0)

    return x_train, x_valid, y_train, y_valid
    

