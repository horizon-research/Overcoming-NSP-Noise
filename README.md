# Overcoming NSP Noise
A project aimed to overcome thermal noise generated by the heat of near sensor processing using a neural network trained on images with high amounts of thermal noise.
This project is being carried out as an independent study which has started in the spring of 2022. 

#### Collaborators
Christopher Bruinsma and Yuhao Zhu at Horizon Research, Univerisity of Rochester

## Capture
Images will be captured using a FLIR BlackFly 3 camera which has thermal-noise induced using a heat-gun. 
The safety of heating the camera will be safely heated using Python code which relies on the Spinnaker SDK from FLIR.

This script is called ```HeatTrigger.py```, it is essentially a camera trigger that triggers based on heat. 

#### Depends on

```python
import PySpin
import sys
import time
```

#### Runs as 
```$ Python3 HeatTrigger.py```

Main additions to FLIR SDK example ```Trigger.py``` are :

For the device temperature: ```GetCameraTemperature(cam)``` :

```python
def GetCameraTemperature(cam):
    x = 0
    if cam.DeviceTemperature.GetAccessMode() == PySpin.RO:
        x = cam.DeviceTemperature.ToString()
    x = float(x)
    return x
```
as well as:  ```Go(cam,GoalTemperature)```

```python
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

```python
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
Images are saved as  ```sample-serialNumber-capNum-temp.png```

The numbering relies on the ```CamConfig.json``` which stores the number of captures after each capture. 
In the terminal it looks like the following 
```
...
$ Acquiring images...
$ Image saved at sample-18255214-12-39.png

$ Image saved at sample-18255214-13-39.png

$ Trigger mode disabled...
...
```



## Neural Network
Due to the nature of image processing of noisy images, max-pooling will likely be used alongside some kind of edge dectection algorthim. This aspect very much remains in the research stage, but as of right now the goal is to train a Convolution Neural Network to indentify cups of coffee that have my name on them. 

#### Runs as
```$ IgnoresThermal.py``` 

#### Intent 
Indentify cups of coffee that have my name on them. This will be done using a variety of coffee cups the on-campus Starbucks here at the Univeristy. 
These are contained withing the ```Training_Data``` folder

#### Depends on

```python
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers
```
As well as ```pydot``` and ```graphviz```

#### When Running 
```
...
2/2 [==============================] - 5s 2s/step - loss: 0.0096 - accuracy: 1.0000 - val_loss: 0.8539 - val_accuracy: 0.4667
Epoch 46/50
2/2 [==============================] - 5s 2s/step - loss: 0.0044 - accuracy: 1.0000 - val_loss: 0.8647 - val_accuracy: 0.4667
Epoch 47/50
2/2 [==============================] - 5s 3s/step - loss: 0.0036 - accuracy: 1.0000 - val_loss: 0.8761 - val_accuracy: 0.4667
Epoch 48/50
2/2 [==============================] - 5s 3s/step - loss: 0.0024 - accuracy: 1.0000 - val_loss: 0.8887 - val_accuracy: 0.4667
Epoch 49/50
2/2 [==============================] - 6s 3s/step - loss: 0.0085 - accuracy: 1.0000 - val_loss: 0.9023 - val_accuracy: 0.4667
Epoch 50/50
2/2 [==============================] - 5s 3s/step - loss: 0.0023 - accuracy: 1.0000 - val_loss: 0.9174 - val_accuracy: 0.4667
This image is 77.95 your coffee.
...
```

### Works Cited :
> Dynamic Temperature Management of Near-Sensor Processing for Energy-Efficient High-Fidelity 
    Imaging. Kodukula Et Al.

> Dirty Pixels: Towards End-to-End Image Processing and Perception Diamond Et. Al.

> FLIR. (n.d.). Spinnaker-SDKVersion (Trigger.py). Spinnaker SDK. Retrieved from https://www.flir.com/products/spinnaker-sdk/. 

> FLIR Integrated Imaging Solutions, Inc. (n.d.). PySpinDoc. 

> Team, K. (n.d.). Keras documentation: Image Classification From Scratch. Keras. Retrieved February 22, 2022, from 
   https://keras.io/examples/vision/image_classification_from_scratch/ 
