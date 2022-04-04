# For use in CSC 391 by : Christopher Bruinsma | used for FLIR BlackFly S. Camera
# Used : For CSC 391 Spring 2022. Overcoming NSP Part I | Automatition 
# Cites : Trigger.py from FLIR Teledyne all rights reserved. 

from platform import node
import PySpin
import json
import os
import time
import sys
import CameraNexus as Nexus

Take = 5 # Five pictures at each go around 

class Trigger:
    SOFTWARE = 1
    HARDWARE = 2

def ConfigureForCapture():
    Accuracy = open("Accuracy.json","r")
    load = json.load(Accuracy)
    image_num_config = int(load("NumPhotos"))
    Accuracy.close
    return image_num_config
   
def AfterCapture():
    Accuracy = open("Accuracy.json","w")
    load = json.load(Accuracy)
    load["NumPhotos"] = int(load["NumPhotos"]) + Take
    json.dump(load,Accuracy)

def GetImages(cam, nodemap, transport):
   ImageNum =  ConfigureForCapture()
   
   ContinuousCapture = PySpin.CEnumEntryPtr(nodemap.GetNode('AcquisitionMode'))
   ContinuousCapture.SetIntValue(ContinuousCapture.GetEntryByName('Continuous').GetValue())

   cam.BeginAcquisition()
   print('Acquiring images...')
   SerialNum = PySpin.CStringPtr(transport.GetNode('DeviceSerialNumber')).GetValue()

   for i in range(Take):
       time.sleep(5) # Allows the user to move the camera / object after each captur e
       Exec(nodemap) 
       image = cam.GetNextImage(1000)

       if SerialNum:
            filename = 'sample-%s-%d-%d.png' % (SerialNum, i +
                                                            ImageNum, Nexus.GetCameraTemperature(cam))
       else:  # if serial number is empty
            filename = 'sample-%d.png' % i + str(ImageNum) 

       image.Save(filename)
       image.Release()
       print('Image saved at %s\n' % filename)
   AfterCapture() # Save the number of images taken 
   cam.EndAcquisiton()

def Reset(nodemap):
    TriggerMode = PySpin.CEnumEntryPtr(nodemap.GetNode('TriggerMode'))
    TriggerMode.SetIntValue(TriggerMode.GetEntryByName('Off').GetValue())
 
def DirectorOfPhotography(cam):
    transportLayer = cam.GetTLDeviceNodeMap()
    
    cam.Init()
    
    nodemap = cam.GetNodeMap()
    GetImages(cam,nodemap,transportLayer)
    Reset(nodemap)
    
    cam.DeInit()

def TriggerReset(nodemap):
    # Turn the Trigger Off
    TriggerMode = PySpin.CEnumEntryPtr(nodemap.GetNode('TriggerMode'))
    
    TriggerMode.SetIntValue(
        TriggerMode.GetEntryByName('Off').GetValue()
    )
    # Chages its trigger to software
    TriggerSelector = PySpin.CEnumEntryPtr(nodemap.GetNode('TriggerSource'))
    
    TriggerSelector.SetIntValue(
        TriggerSelector.GetEntryByName('Software').GetValue()
    )

    # Turn the Trigger back on. 

    TriggerMode.SetIntValue(
        TriggerMode.GetEntryByName('On').GetValue()
    )

def Exec(nodemap):
    Executor = PySpin.CCommandPtr(nodemap.GetNode('TriggerSource'))
    Executor.Execute()

def main():
    system = PySpin.System.GetInstance()
    cameras = system.GetCameras()
    Number = cameras.GetSize()
    print('Number of cameras detected: %d' % Number)

if __name__ == '__main__':
    if main():
        sys.exit(0)
    else:
        sys.exit(1)