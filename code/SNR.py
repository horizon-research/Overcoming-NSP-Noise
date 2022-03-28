"""
This is a script used to find the SNR of this dataset as a metric for how clean or un-clean the images are.
Cites : Yuhao Zhu CSC 292 / 572 Lecture
"""



import sys
import numpy as np #Helps with Array Operations
from PIL import Image #Helps with combining the images
import cv2
from scipy import stats


def SNR(Image):
    img = cv2.imread(Image)
    Array = np.asanyarray(img)
    ArrayMean = np.mean(Array)
    ArrayStdev = np.std(Array)
    return 1 / np.log(ArrayMean/ArrayStdev)

print("SNR for an image taken at 90°C by FLIR BFS: ",SNR('Demolished.jpg'),"\n")
print("SNR for an image taken at 90°C by FLIR BFS: ",SNR('sample-18255214-1801-90.png'),"\n")
print("SNR for an image taken at 90°C by an Olympus OMD EM1-II at nominal conditions: ",SNR('ICED4.jpg'),"\n")







