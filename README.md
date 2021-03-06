# Overcoming NSP Noise

Overcoming NSP Noise is an independent project investigating the efficacy of machine learning on images taken on cameras under high thermal load. The project has two main parts, one is establishing an automated image capture system, and two is to generate a high quantity of  images using this automated setup for the training of a noisy-image-trained neural network.


#### Collaborators

Christopher Bruinsma and Yuhao Zhu at Horizon Research, *University of Rochester*

## Image Capture

Images will be captured using a [FLIR BlackFly USB3](https://www.flir.com/products/blackfly-s-usb3/) camera which has thermal-noise induced using a heat gun from [Wagner](https://www.wagnerspraytech.com/products/heat-guns/ht400-heat-gun/).

In order to safely heat the camera,  Python code is used which relies on the [Spinnaker SDK](https://www.flir.com/products/spinnaker-sdk/) to monitor the camera temperature which is limited by the camera to less than 100°C. The heat gun is also automated around the temperature of the camera. This is achieved through the use of [Python-Kasa](https://python-kasa.readthedocs.io/en/latest/) which will power on and off the heat-gun by turning on and off a [Smart-Plug](https://www.kasasmart.com/us/products/smart-plugs)

Dependencies

```
Python3.8
sys
asyncio     : pip install asyncio 
tensorflow  : pip install tensorflow 
poetry      : pip install poetry 
json
PySpin      : pip install spinnaker_python-2.6.0.156-cp38-cp38-macosx_10_14_x86_64.whl 
kasa        : pip install kasa
keras       : pip install keras
time
graphviz    : pip install graphviz
pydot       : pip install pydot
numpy       : pip install numpy
PIL
cv2         : pip install cv2
       
```

![](https://github.com/horizon-research/Overcoming-NSP-Noise/blob/182410a5e75a21ba176fb49616ff4616c97eafb7/docs/Main.jpg)

### Code
Under the alias of [HeatTrigger.py](https://github.com/horizon-research/Overcoming-NSP-Noise/blob/b6b2682504cde2be44bf4a3e9def78783bd7c998/code/Camera%20Code/HeatTrigger.py) this code adds on to the code written by the Spinnaker SDK ```Trigger.py```

This was added to dynamically access the camera temperature **:** ```GetCameraTemperature(cam)``` 

```python
def GetCameraTemperature(cam):
    if cam.DeviceTemperature.GetAccessMode() == PySpin.RO:
        return float(cam.DeviceTemperature.ToString())
```

I have added as well:  ```Heat(cam,GoalTemperature)``` which is run inside of ```Capture(cam,temp)```*(below)*

```python
# Does the temperature sensing during the loops.
def Heat(cam, GoalTemperature):
    # Get Temperature of Camera
    Temp = GetCameraTemperature(cam)
    # Heating
    if Temp > GoalTemperature + 2.5:
        return False

    else:
        asyncio.run(HeatGun.On()) 
        """
            Continue Heating unitl goal temperature is achieved
        """
        TempBar = Bar('Heating',fill='█',index=Temp,max=GoalTemperature)
        while Temp < GoalTemperature:
            Temp = GetCameraTemperature(cam)
            time.sleep(2)
            TempBar.next(BarProgress(GetCameraTemperature(cam),Temp))
        TempBar.finish()
        asyncio.run(HeatGun.Off())
        return True
```

```python
def Capture(cam,temp):
    """
    This function acts as the body of the example; please see NodeMapInfo example
    for more in-depth comments on setting up cameras.

    :param cam: Camera to run on.
    :type cam: CameraPtr
    :return: True if successful, False otherwise.
    :rtype: bool
    """
    try:
        result = True
        # Retrieve TL device nodemap and print device information
        nodemap_tldevice = cam.GetTLDeviceNodeMap()
        cam.Init()
        # Retrieve GenICam nodemap
        nodemap = cam.GetNodeMap()

        # Configure trigger
        if configure_trigger(cam) is False:
            return False
        result &= AutoExposure(cam)
        if(Heat(cam,temp)):
             # Acquire images
            result &= acquire_images(cam, nodemap, nodemap_tldevice)
            # Reset trigger
            result &= reset_trigger(nodemap)
            cam.DeInit()
            result = True
        else:
            print('\
                Camera is %d°C your temperature was %s°C, please allow the camera to cool and try again.'  
            % (GetCameraTemperature(cam),temp))
            cam.DeInit()
            return False
    except PySpin.SpinnakerException as ex:
        print('Error: %s' % ex)
        result = False

    return result
```

Heat Gun Automation

```python
class HeatGun:
    async def On():
        print("Heat Gun Power On")
        HeatGun = s.SmartPlug('192.168.0.1')
        await HeatGun.turn_on()

    async def Off():
        print("Heat Gun Power Off")
        HeatGun = s.SmartPlug('192.168.0.1')
        await HeatGun.turn_off()
```
    
  
The heat testing is done using a loop in the ```main()``` method.

```python
    for i, cam in enumerate(cam_list):
        try: 
            if(Capture(cam,int(argv))):    
                print('Capture Completed.')
        except PySpin.SpinnakerException as ex:
            print('Capture Failed.')
            break
    del cam # It's about the little things in programming...
```

#### Runs as 
```$ Python3.8 HeatTrigger.py temperature```

The numbering relies on the ```Accuracy.json``` which stores the number of captures after each capture.
In the terminal it looks like the following:

#### Example Capture 

Cold to Hot
```
$ Python3.8 HeatTrigger.py 48
...

Heat Gun Power On
Heating |████████████████████████████████| 48/48

Heat Gun Power Off

Acquiring images...
Image saved at sample-18255214-2913-48.png

Image saved at sample-18255214-2914-48.png

Image saved at sample-18255214-2915-48.png

Image saved at sample-18255214-2916-48.png

Image saved at sample-18255214-2917-49.png

Trigger mode disabled...
Capture Completed.
```

#### Example Capture
Over Temperature

```
$ Python3.8 HeatTrigger.py 25
...
Camera is 49°C your temperature was 25°C, please allow the camera to cool and try again.
Capture Failed.
```




#### Metrics 
The main metric measured for images in this project is the [Signal-To-Noise](https://github.com/horizon-research/Overcoming-NSP-Noise/blob/b6b2682504cde2be44bf4a3e9def78783bd7c998/code/Metrics/SNR.py) ratio of these images. This is done using ```SNR.py```

<!-- The SNR is taken as follows 

**SNR**<sub>TempSet</sub> =  &Sigma;(&mu;<sub>ImagePixels</sub> / &sigma;<sub>ImagePixels</sub>)

### This is the SNR of the Data Set Overall

|Temperature Set | 60 Degree   |   70 Degree | 80 Degree   |   90 Degree |
| ----------- | ----------- | ----------- | ----------- | ----------- |
| **Signal to Noise** | 2.973    | 3.595       | 3.649  | 3.333 |


#### This is the SNR of the Cold Coffee Training set

|Temperature Set | 60 Degree   |   70 Degree | 80 Degree   |   90 Degree |
| ----------- | ----------- | ----------- | ----------- | ----------- |
| **Signal to Noise** | 3.005     | 2.566        | 2.481   | 2.696  |


#### This is the SNR for the Hot Coffee Training Set

|Temperature Set | 60 Degree   |   70 Degree | 80 Degree   |   90 Degree |
| ----------- | ----------- | ----------- | ----------- | ----------- |
| **Signal to Noise** | 2.88     | 4.236        | 4.117   | 3.91   | -->


<!-- While this might be counterintuitive, the rise in signal-to-noise ratio, it can be accounted for the use of different exposure compensation settings. For example, images taken with at f16 show quite a bit more noise than images taken at f2. Given that the hot images were mostly taken at f2 by combining them with the cold images the signal to noise ratio is much higher. Noise is always more evident at longer exposures and when there is less light on the sensor.  -->

 
## Machine Learning
Due to the nature of image processing of noisy images, max-pooling will likely be used alongside some kind of edge detection algoritm. This aspect very much remains in the research stage, but as of right now the goal is to train a Convolution Neural Network to identify cups of coffee that are either hot or iced. 
This implementation relies on [TensorFlow.Keras](https://keras.io).

This machine-learning model relies heavily on the **ResNet** model and has 34 layers which use the implementation of residual being added back. 

#### Runs as
```$ IgnoresThermal.py``` and ```$ NoThermal.py```

#### Intent 
Identify cups of coffee as either iced or hot. This will be done using a variety of coffee cups from the on-campus Starbucks here at the University that contain hot or iced coffee. These are contained within the ```Training_Data``` and ```CleanTestImages``` folders. 

#### The Code

I have done the following to create a neural network that uses data augmentation to virtually increase the sample size, as well as varying sized 
convolution kernels, batch normalization, making more dense the layers of the network and finally dropping layers out at each iteration to help train the network of more key characteristics. 

```python 
""" Citations: 

Cites: https://towardsdatascience.com/an-overview-of-resnet-and-its-variants-5281e2f56035
"""
def Block(x,size):
      x = layers.Activation("sigmoid")(x)
      x = layers.Conv2D(size, 3, strides=2, padding="same")(x)
      return layers.BatchNormalization()(x)

def SixtyFour(x):
    for i in range(0,3):
        x = Block(x,64)
        previous_block_activation = x 
        residual = layers.Conv2D(64, 3, strides=2, padding="same")(
            previous_block_activation
        )
        x = Block(x,64)
        x = layers.add([x, residual])  # Add back residual
        previous_block_activation = x 
        x = layers.Dropout(0.3)(x)

    return x     

def OneTwentyEight(x):
    for i in range(0,4):
        x = Block(x,128)
        previous_block_activation = x 
        residual = layers.Conv2D(128, 3, strides=2, padding="same")(
            previous_block_activation
        )
        x = Block(x,128)
        x = layers.add([x, residual])  # Add back residual
        previous_block_activation = x 
        x = layers.Dropout(0.3)(x)
    return x            

def TwoFiftySix(x):
    for i in range(0,6):
        x = Block(x,256)
        previous_block_activation = x 
        residual = layers.Conv2D(256, 3, strides=2, padding="same")(
            previous_block_activation
        )
        x = Block(x,256)
        x = layers.add([x, residual])  # Add back residual
        previous_block_activation = x 
        x = layers.Dropout(0.3)(x)        
    return x         

def FiveTwelve(x):
    for i in range(0,3):
        x = Block(x,512)
        previous_block_activation = x 
        residual = layers.Conv2D(512, 3, strides=2, padding="same")(
            previous_block_activation
        )
        x = Block(x,512)
        x = layers.add([x, residual])  # Add back residual
        previous_block_activation = x 
        x = layers.Dropout(0.3)(x)
    return x                

"""
Assembling the model
"""
def NModel(input_shape, num_classes):
    inputs = keras.Input(shape=input_shape)
    # Image augmentation block
    # Entry block
    """
    This is a modified ResNet Model
    """
    x = data_augmentation(inputs)
    x = layers.Rescaling(1.0 / 255)(x)
    x = layers.Conv2D(64, 7, strides=2, padding="same")(x)
    x = (lambda x: FiveTwelve(TwoFiftySix(OneTwentyEight(SixtyFour(x)))))(x)
    x = layers.Rescaling(1.0 / 2)(x)
    x = (lambda x: FiveTwelve(TwoFiftySix(OneTwentyEight(SixtyFour(x)))))(x)
    x = layers.GlobalAveragePooling2D()(x)

    if num_classes == 2:
        activation = "sigmoid"
        units = 1
    else:
        activation = "softmax"
        units = num_classes

    x = layers.Dropout(0.5)(x)
    outputs = layers.Dense(units, activation=activation)(x)
    return keras.Model(inputs, outputs)

```

#### When Running 

```
2022-03-03 00:26:01.678284: I tensorflow/core/platform/cpu_feature_guard.cc:151] This TensorFlow binary is optimized with oneAPI Deep Neural Network Library (oneDNN) to use the following CPU instructions in performance-critical operations:  AVX2 FMA
To enable them in other operations, rebuild TensorFlow with the appropriate compiler flags.
Found 599 files belonging to 2 classes.
Using 119 files for validation.
Please Enter 1 for compile 2 for test and 3 for both or and key to close
2
Current accuracy is 0.537177: 
You have selected test
Images of hot coffee
This image is 83.03 percent hot coffee and this image is 16.97 percent iced coffee.
This image is hot coffee

This image is 59.49 percent hot coffee and this image is 40.51 percent iced coffee.
This image is hot coffee

Images of iced coffee
This image is 16.03 percent hot coffee and this image is 83.97 percent iced coffee.
This image is cold coffee

This image is 41.25 percent hot coffee and this image is 58.75 percent iced coffee.
This image is cold coffee

Current final accuracy is 0.550496: 
```

### Analysis
*Too soon to be determined*. Images only number 600 and overfitting is quite a risk. 

### **Works Cited** :
> Dirty Pixels: Towards End-to-End Image Processing and Perception Diamond Et. Al.

> Dynamic Temperature Management of Near-Sensor Processing for Energy-Efficient High-Fidelity 
    Imaging. Kodukula Et Al.

> Feng, Vincent. 2017. “An Overview of ResNet and its Variants | by Vincent Feng.” Towards Data Science. https://towardsdatascience.com/an-overview-of-resnet-and-its-variants-5281e2f56035.

> FLIR. (n.d.). Spinnaker-SDKVersion (Trigger.py). Spinnaker SDK. Retrieved from https://www.flir.com/products/spinnaker-sdk/. 

> FLIR. (n.d.). Spinnaker-SDKVersion (Exposure_QuickSpin.py). Spinnaker SDK. Retrieved from https://www.flir.com/products/spinnaker-sdk/. 

> FLIR. (n.d.). Spinnaker-SDKVersion (ImageFormatControl_QuickSpin.py). Spinnaker SDK. Retrieved from https://www.flir.com/products/spinnaker-sdk/. 

> FLIR Integrated Imaging Solutions, Inc. (n.d.). PySpinDoc. 

> François Chollet, Team, K. (n.d.). Keras documentation: Image Classification From Scratch. Keras. Retrieved February 22, 2022, from 
   https://keras.io/examples/vision/image_classification_from_scratch/ 

> n.d. python-kasa — python-kasa documentation. Accessed April 5, 2022. https://python-kasa.readthedocs.io/en/latest/.

> University of Rochester and Yuhao Zhu. n.d. “Lecture 8: Image Sensing and Sensor Design II.” Fall 2021. Rochester, New York. Accessed March, 2022. https://www.cs.rochester.edu/courses/572/fall2020/decks/sensor-2.pd
