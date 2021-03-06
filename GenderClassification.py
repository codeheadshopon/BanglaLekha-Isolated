from __future__ import print_function
from keras.layers import Input, Dense, Convolution2D, MaxPooling2D, UpSampling2D
from keras.models import Model
import matplotlib.pyplot as plt
import numpy as np

np.random.seed(1337)  # for reproducibility
from keras import  callbacks
from keras.datasets import mnist,cifar10
from keras.models import Sequential
from keras.layers import Dense, Dropout, Activation, Flatten
from keras.layers import Convolution2D, MaxPooling2D
from keras.utils import np_utils
from PIL import Image
from os import listdir
from keras.models import load_model
from os.path import isfile, join
import PIL.ImageOps
import matplotlib.cm as cm
import numpy as np
from skimage import color
from skimage import io
import pickle
# import cv
import cv2
import matplotlib.pyplot as plt
import os
from keras.preprocessing.image import ImageDataGenerator
from matplotlib import pyplot
from keras.regularizers import l2, activity_l2
from keras.datasets import mnist,cifar10
from keras.models import Sequential
from keras.layers import Dense, Dropout, Activation, Flatten
from keras.layers import Convolution2D, MaxPooling2D
from keras.utils import np_utils
from PIL import Image
from os import listdir
from keras.models import load_model
from os.path import isfile, join
import PIL.ImageOps
import matplotlib.cm as cm
import numpy as np
from keras.callbacks import ModelCheckpoint
from skimage import color
from skimage import io
import pickle
# import cv
import cv2
import matplotlib.pyplot as plt
import os
from keras.preprocessing.image import ImageDataGenerator
from matplotlib import pyplot
from keras.regularizers import l2, activity_l2
from skimage.transform import resize
import scipy
from keras.callbacks import TensorBoard
from skimage.transform import resize
import scipy
from keras.callbacks import TensorBoard
import cPickle,gzip,sys

import random

import matplotlib.pyplot as plt
from skimage.feature import hog
from skimage import data, color, exposure
from scipy.spatial import distance
import math
from sklearn.metrics.pairwise import euclidean_distances


def dataset_load(path):
    if path.endswith(".gz"):
        f=gzip.open(path,'rb')
    else:
        f=open(path,'rb')

    if sys.version_info<(3,):
        data=cPickle.load(f)
    else:
        data=cPickle.load(f,encoding="bytes")
    f.close()
    return data

data, dataLabel, dataMarking, imageFullName = dataset_load('./FullData.pkl.gz')
Max=0
print(imageFullName[0])
for i in range(len(dataLabel)):
    Max=max(Max,dataLabel[i])


''' This Portion is for Labeling and Dividing the dataset. Each sample Contains 1800 Images. Total 84 Samples '''    
X_train = []
X_test = []
y_train=[]
y_test=[]

from collections import defaultdict
Dict=defaultdict(lambda:None)

for i in range(len(dataLabel)):
    if(Dict[dataLabel[i]] is None):
        Dict[dataLabel[i]]=1
    else:
        Dict[dataLabel[i]]=Dict[dataLabel[i]]+1

    if(Dict[dataLabel[i]]>1800):
        X_test.append(data[i])
        X=imageFullName[i]
        Label=int(X[8])
        y_test.append(Label)
    else:
        X_train.append(data[i])
        X = imageFullName[i]
        Label = int(X[8])
        y_train.append(Label)

batch_size = 128
nb_classes = 2
nb_epoch = 15

# input image dimensions
img_rows, img_cols = 56, 56
# number of convolutional filters to use
nb_filters = 32
# size of pooling area for max pooling
nb_pool = 2
# convolution kernel size
kernel_size = (5, 5)

X_train=np.asarray(X_train)
X_test=np.asarray(X_test)
X_train = X_train.reshape(X_train.shape[0], 1, img_rows, img_cols)
X_test = X_test.reshape(X_test.shape[0], 1, img_rows, img_cols)
X_train = X_train.astype('float32')
X_test = X_test.astype('float32')
X_train /= 255
X_test /= 255
print('X_train shape:', X_train.shape)
print(X_train.shape[0], 'train samples')
print(X_test.shape[0], 'test samples')

Y_train = np_utils.to_categorical(y_train, nb_classes)
Y_test = np_utils.to_categorical(y_test, nb_classes)

model = Sequential()

model.add(Convolution2D(nb_filters, kernel_size[0], kernel_size[1],
                        border_mode='valid',
                        input_shape=(1, img_rows, img_cols)))
model.add(Activation('relu'))
model.add(Convolution2D(nb_filters, kernel_size[0], kernel_size[1]))
model.add(Activation('relu'))
model.add(Convolution2D(nb_filters+32, kernel_size[0], kernel_size[1]))
model.add(Activation('relu'))

model.add(MaxPooling2D(pool_size=(nb_pool, nb_pool)))
model.add(Dropout(0.5))

model.add(Flatten())
model.add(Dense(128))
model.add(Activation('relu'))
model.add(Dropout(0.25))
model.add(Dense(nb_classes))
model.add(Activation('softmax'))

model.compile(loss='binary_crossentropy',
              optimizer='adadelta',
              metrics=['accuracy'])

model.fit(X_train, Y_train, batch_size=batch_size, nb_epoch=nb_epoch,
          verbose=1, validation_data=(X_test, Y_test))
score = model.evaluate(X_test, Y_test, verbose=0)
print('Test score:', score[0])
print('Test accuracy:', score[1])
print('Parameters: ', model.count_params())
print(model.summary())


