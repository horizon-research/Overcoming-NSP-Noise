"""
This is a script used to find the SNR of this dataset as a metric for how clean or un-clean the images are.
Cites : Yuhao Zhu CSC 292 / 572 Lecture
"""



import sys
import os
import json
import numpy as np #Helps with Array Operations
from PIL import Image #Helps with combining the images
import cv2
from scipy import stats



def SNR(Image):
    """
    param: Image, takes and image as an array and takes the SNR of the image using mean / std
    returns : SNR of the image
    """
    img = cv2.imread(Image)
    Array = np.asanyarray(img)
    ArrayMean = np.mean(Array)
    ArrayStdev = np.std(Array)
    return np.log(ArrayMean/ArrayStdev)

def SUM(path):
    SUM = 0
    COUNT = 0
    for img in os.listdir(path):
        f = os.path.join(path,img)
        if os.path.isfile(f):
          if(f.__contains__(".png")):
              SUM+=SNR(f)
              COUNT+=1
    return SUM / COUNT


def main():
    path = 'Training_Data/Hot/training/'
    print("The SNR for the Hot Training Images",SUM(path),"\n")

    path = 'Training_Data/Cold/training/'
    print("The SNR for the Cold Training Images",SUM(path),"\n")

    print("The SNR for a test image, taken on an Olympus OMD EM1-II", SNR("ICED4.jpg"),"\n")
    print("The SNR for an image taken at 90°C by FLIR BFS: ",SNR('sample-18255214-1801-90.png'),"\n")
   
if __name__ == "__main__":
    main()


