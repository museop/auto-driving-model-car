import numpy as np
from keras.models import Sequential
from keras.models import load_model
from keras.optimizers import Adam
from keras.callbacks import ModelCheckpoint
from keras.layers import Lambda, Conv2D, MaxPooling2D, Dropout, Dense, Flatten
from keras import backend as K
from utility import INPUT_SHAPE, preprocess, load_data, batch_generator
import os


class SteeringModel(object):
    def __init__(self):
        self.model = None
        
        
    def build_model(self, keep_prob=0.5):
        if self.model != None:
            del self.model
            K.clear_session()
            
        self.model = Sequential()
        self.model.add(Lambda(lambda x: x/127.5-1.0, input_shape=INPUT_SHAPE))
        self.model.add(Conv2D(24, 5, 5, activation='elu', subsample=(2, 2)))
        self.model.add(Conv2D(36, 5, 5, activation='elu', subsample=(2, 2)))
        self.model.add(Conv2D(48, 5, 5, activation='elu', subsample=(2, 2)))
        self.model.add(Conv2D(64, 3, 3, activation='elu'))
        self.model.add(Conv2D(64, 3, 3, activation='elu'))
        self.model.add(Dropout(keep_prob))
        self.model.add(Flatten())
        self.model.add(Dense(100, activation='elu'))
        self.model.add(Dense(50, activation='elu'))
        self.model.add(Dense(10, activation='elu'))
        self.model.add(Dense(1))
        self.model.summary()
        
        
    def load_model_from(self, model_h5_file):
        if self.model != None:
            del self.model
            K.clear_session()
            
        self.model = load_model(model_h5_file)
    
    
    def train_model(self, data_dir, learning_rate, batch_size, samples_per_epoch, nb_epoch, test_size):
        x_train, x_valid, y_train, y_valid = load_data(data_dir, test_size)
        
        checkpoint = ModelCheckpoint(
            'steering_model-{epoch:03d}.h5',
            monitor='val_loss',
            verbose=0,
            save_best_only=True,
            mode='auto')
            
        self.model.compile(
            loss='mean_squared_error',
            optimizer=Adam(lr=learning_rate))
            
        self.model.fit_generator(
            batch_generator(data_dir, x_train, y_train, batch_size, True),
            samples_per_epoch,
            nb_epoch,
            max_q_size=1,
            validation_data=batch_generator(data_dir, x_valid, y_valid, batch_size, False),
            nb_val_samples=len(x_valid),
            callbacks=[checkpoint],
            verbose=1)
    
    
    def predict(self, image):
        image = preprocess(image)
        image = np.array([image])
        steering_angle = float(self.model.predict(image, batch_size=1))
        return steering_angle
    
    
    def __del__(self):
        if self.model != None:
            del self.model
            K.clear_session()  

