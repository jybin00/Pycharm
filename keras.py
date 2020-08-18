from keras.datasets import mnist
from keras import models
from keras import layers
from keras.utils import to_categorical

(train_images, train_lables), (test_images, test_lables) = mnist.load_data()


