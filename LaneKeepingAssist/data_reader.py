import scipy.misc
import random

DATA_DIR = '/home/nvidia/Desktop/Workspace/driving_dataset/'

class DataReader(object):
    def __init__(self, data_dir=DATA_DIR):
        self.load()

    def load(self):
        xs = []
        ys = []

        self.train_batch_pointer = 0
        self.val_batch_pointer = 0

        with open(DATA_DIR + 'data.txt') as f:
            for line in f:
                xs.append(DATA_DIR + line.split()[0])
                ys.append(float(line.split()[1]) * scipy.pi / 180)

        self.num_images = len(xs)

        c = list(zip(xs, ys))
        random.shuffle(c)
        xs, ys = zip(*c)

        self.train_xs = xs[:int(len(xs) * 0.8)]
        self.train_ys = ys[:int(len(ys) * 0.8)]

        self.val_xs = xs[-int(len(xs) * 0.2):]
        self.val_ys = ys[-int(len(ys) * 0.2):]

        self.num_train_images = len(self.train_xs)
        self.num_val_images = len(self.val_xs)

    def load_train_batch(self, batch_size):
        x_out = []
        y_out = []

        for i in range(0, batch_size):
            image = scipy.misc.imread(self.train_xs[(self.train_batch_pointer + i) % self.num_train_images]) 
            x_out.append(scipy.misc.imresize(image[-150:], [66, 200]) / 255.0)
            y_out.append([self.train_ys[(self.train_batch_pointer + i) % self.num_train_images]])
        self.train_batch_pointer += batch_size
		
        return x_out, y_out

    def load_val_batch(self, batch_size):
        x_out = []
        y_out = []

        for i in range(0, batch_size):
            image = scipy.misc.imread(self.val_xs[(self.val_batch_pointer + i) % self.num_val_images])
            x_out.append(scipy.misc.imresize(image[-150:], [66, 200]) / 255.0)
            y_out.append([self.val_ys[(self.val_batch_pointer + i) % self.num_val_images]])
        self.val_batch_pointer += batch_size
		
        return x_out, y_out

