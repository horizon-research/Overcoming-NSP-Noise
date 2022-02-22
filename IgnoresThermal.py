# This will be the Neural Network Script
import pathlib
import tensorflow as tf
from tensorflow import keras

images = [] # DataSet of Images

def main() :
    images = [] #Create DataSet
    for path in pathlib.Path("Training_Data/Refresh").iterdir():
        if path.is_file():
            current_file = open(path, "r")
            images.append(current_file)
            current_file.close()

    for path in pathlib.Path("Training_Data/BOSE").iterdir():
        if path.is_file():
            current_file = open(path, "r")
            images.append(current_file)
            current_file.close()

    for path in pathlib.Path("Training_Data/WhiteCup").iterdir():
        if path.is_file():
            current_file = open(path, "r")
            images.append(current_file)
            current_file.close()

    print("There are",len(images),"images in the dataset")

if __name__ == '__main__':
    main()





