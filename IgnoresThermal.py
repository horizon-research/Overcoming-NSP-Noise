# This will be the Neural Network Script
import pathlib
import tensorflow as tf
from tensorflow import keras

images = [] # DataSet of Images

image_size = (180, 180)
batch_size = 32

DataSet = tf.keras.preprocessing.image_dataset_from_directory(
    "Training_Data",
    validation_split=0.2,
    subset="training",
    seed=1337,
    image_size=image_size,
    batch_size=batch_size,
)

Validation = tf.keras.preprocessing.image_dataset_from_directory(
    "Training_Data",
    validation_split=0.2,
    subset="validation",
    seed=1337,
    image_size=image_size,
    batch_size=batch_size,
)

def main() :
    print("Success")





if __name__ == '__main__':
    main()





