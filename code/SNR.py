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
    return ArrayMean/ArrayStdev

def SNR_SUM(path):
    SUM = 0
    COUNT = 0
    for img in os.listdir(path):
        f = os.path.join(path,img)
        if os.path.isfile(f):
          if(f.__contains__(".png")):
              SUM+=SNR(f)
              COUNT+=1
          elif(f.__contains__(".jpg")):
              SUM+=SNR(f)
              COUNT+=1    
    return SUM / COUNT


def main():
    path = 'NoiNN/Training_Data/Hot/training/'
    print("The SNR for the Hot Training Images",SNR_SUM(path),"\n")
    path = 'NoiNN/Training_Data/Cold/training/'
    print("The SNR for the Cold Training Images",SNR_SUM(path),"\n")

    path = 'CLNN/CleanTestImages/Hot/training/'
    print("The SNR for the Clean Hot Training Images",SNR_SUM(path),"\n")
    path = 'CLNN/CleanTestImages/Cold/training/'
    print("The SNR for the CLean  Cold Training Images",SNR_SUM(path),"\n")
   
if __name__ == "__main__":
    main()


