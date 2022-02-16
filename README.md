# Overcoming NSP Noise
A project aimed to overcome thermal noise generated by the heat of near sensor processing using a neural network trained on images with dark-current-induced noise.
This project is being carried out as an independent study which has started in the spring of 2022. 

#### Collaborators
Christopher Bruinsma and Yuhao Zhu at Horizon Research, Univerisity of Rochester

## First : Capture
Images will be captured using a FLIR BlackFly 3 Camera which has noise induced using a heat-gun. The safety of heating the camera will be safely heated using Python code which relies on the Spinnaker SDK from FLIR.

This script is called HeatSafety.py, it is essentially a camera trigger that triggers based on heat. 
#### Depends on:

```ruby
import PySpin
import sys
import time
```

#### Runs as: 
```> Python3 HeatTrigger.py```

Main additions to FLIR SDK example ```Trigger.py``` are:

for the device temperature: ```GetCameraTemperature(cam)```

```ruby
def GetCameraTemperature(cam):
    x = 0
    if cam.DeviceTemperature.GetAccessMode() == PySpin.RO:
        x = cam.DeviceTemperature.ToString()
    x = float(x)
    return x
```
as well as:  ```Go(cam,GoalTemperature)```:
```ruby
def Go(cam, GoalTemperature):
    # Get Temperature of Camera

    Temp = GetCameraTemperature(cam)
    print(GoalTemperature)

    # Heating
    while Temp < GoalTemperature:
        cam.Init()
        Temp = GetCameraTemperature(cam)
        print(Temp)
        time.sleep(3)  # Protects the camera.

    # Capture 2 images
    if Temp > GoalTemperature:
        # cam.DeInit() This makes the who thing crash much more quickly
        print("Capturing, please continue heating")
        Capture(cam)  # Cites : FLIR TELEDYNE
```

The heat testing is done using a loop in the ``` main()``` method. 

```ruby
def main():
    ...
    # List of Cameras
    for i, cam in enumerate(cam_list):
        # List of Temperatures
        for t in range(50, 80, 5):
            # Initiates Capture
            Go(cam, t)
            time.sleep(2)
    
    print("Capture Complete, please cool the camera.")
    ... 
```
Images are saved as : ```sample-serialNumber-capNum-temp.png```

The numbering relies on the ```CamConfig.json``` which stores the number of captures after each capture. 


## Next : Neural Networks
Due to the nature of image processing of noisy images, max-pooling will likely be used alongside some kind of edge dectection algorthim. This aspect very much remains in the research stage. 



### Works Cited :
> [1] Dynamic Temperature Management of Near-Sensor Processing for Energy-Efficient High-Fidelity 
    Imaging. Kodukula Et Al.

> [2] Dirty Pixels: Towards End-to-End Image Processing and Perception Diamond Et. Al.

> FLIR. (n.d.). Spinnaker-SDKVersion (Trigger.py). Spinnaker SDK. Retrieved from https://www.flir.com/products/spinnaker-sdk/. 

> FLIR Integrated Imaging Solutions, Inc. (n.d.). PySpinDoc. 
