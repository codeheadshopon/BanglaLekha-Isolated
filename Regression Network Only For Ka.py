from __future__ import print_function
import numpy as np

np.random.seed(1337)  # for reproducibility
from keras.models import Sequential
from keras.layers import Dense, Dropout, Activation, Flatten
from keras.layers import Convolution2D, MaxPooling2D
import numpy as np
import cPickle,gzip,sys
from skimage.feature import hog
from skimage import data, color, exposure


def HOG_FEATURE(path):
    image=path
    # image = Image.fromarray(path)
    # image=cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
    fd, hog_image = hog(image, orientations=8, pixels_per_cell=(7, 7),
                        cells_per_block=(1, 1),  visualise=True)

    hog_image_rescaled = exposure.rescale_intensity(hog_image, in_range=(0, 0.02))

    return fd

img_rows,img_cols=28,28
batch_size = 128
nb_classes = 10
nb_epoch = 15
# number of convolutional filters to use
nb_filters = 32
# size of pooling area for max pooling
nb_pool = 2
# convolution kernel size
kernel_size = (5, 5)

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

(X_train,y_train),(X_test,y_test)=dataset_load('./Ka_Classification.pkl.gz')

print(X_test[0].shape)
print(X_train[0].shape)

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


model = Sequential()

model.add(Convolution2D(nb_filters, kernel_size[0], kernel_size[1],
                        border_mode='valid',
                        input_shape=(1, img_rows, img_cols)))
model.add(Activation('relu'))
model.add(Convolution2D(nb_filters, kernel_size[0], kernel_size[1]))

model.add(MaxPooling2D(pool_size=(nb_pool, nb_pool)))
model.add(Dropout(0.5))

model.add(Flatten())
model.add(Dense(32))
model.add(Activation('relu'))
model.add(Dense(1))
model.add(Activation('tanh'))

model.compile(loss='mean_squared_error', optimizer='rmsprop')
model.fit(X_train, y_train, batch_size=128, nb_epoch=1, verbose=1)
