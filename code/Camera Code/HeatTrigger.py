
# coding=utf-8
"""
~~~ This script has been heavily modified Spring '22  under the alias of HeatTrigger.py for CSC 391 Part I | Automation ~~~ 
Copyright (c) 2001-2021 FLIR Systems, Inc. All Rights Reserved.
This software is the confidential and proprietary information of FLIR
Integrated Imaging Solutions, Inc. ("Confidential Information"). You
shall not disclose such Confidential Information and shall use it only in
accordance with the terms of the license agreement you entered into
with FLIR Integrated Imaging Solutions, Inc. (FLIR).
FLIR MAKES NO REPRESENTATIONS OR WARRANTIES ABOUT THE SUITABILITY OF THE
SOFTWARE, EITHER EXPRESSED OR IMPLIED, INCLUDING, BUT NOT LIMITED TO, THE
IMPLIED WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR
PURPOSE, OR NON-INFRINGEMENT. FLIR SHALL NOT BE LIABLE FOR ANY DAMAGES
SUFFERED BY LICENSEE AS A RESULT OF USING, MODIFYING OR DISTRIBUTING
THIS SOFTWARE OR ITS DERIVATIVES.
"""

"""
This is the driver script for the experimentation with the FLIR BLACKFLY S Camera
This script relies on the Trigger.py script provided Copyright (c) 2001-2021 FLIR Systems, Inc. All Rights Reserved.

Essentially this script is a temperature trigger for the camera that continues running until all captures are taken 
This Script also draws on Exposure_QuickSpin.py for auto exposure. 
"""
import sys # Camera
import time # Camera
import json # Camera
import asyncio # Heat Gun
import PySpin # Camera 
from progress.bar import Bar # Style , arguably camera safety. 
import kasa as s # Heat Gun
"""
Python Virtual Enviroments can be challenging at times...
This only works with Python3.8. This is crucial. 
"""
"""
Controls power to the heatgun. This whole asyncio thing is going to prove challenging. 
We want these things to work in tandem. Perhaps 
"""
class HeatGun:
    async def On():
        print("Heat Gun Power On")
        HeatGun = s.SmartPlug('192.168.0.1')
        await HeatGun.turn_on()

    async def Off():
        print("Heat Gun Power Off")
        HeatGun = s.SmartPlug('192.168.0.1')
        await HeatGun.turn_off()

# Take five images per temperature
NUM_IMAGES = 5  # number of images to grab

# What type of trigger?
class TriggerType:
    SOFTWARE = 1
    HARDWARE = 2

CHOSEN_TRIGGER = TriggerType.SOFTWARE

# From Spinnaker SDK : Examples : (copyright) FLIR
def configure_trigger(cam):
    """
    This function configures the camera to use a trigger. First, trigger mode is
    set to off in order to select the trigger source. Once the trigger source
    has been selected, trigger mode is then enabled, which has the camera
    capture only a single image upon the execution of the chosen trigger.

     :param cam: Camera to configure trigger for.
     :type cam: CameraPtr
     :return: True if successful, False otherwise.
     :rtype: bool
    """
    result = True

    print('*** CONFIGURING TRIGGER ***\n')
    print(
        'Note that if the application / user software triggers faster than frame time, '
        'the trigger may be dropped / skipped by the camera.\n')
    print(
        'If several frames are needed per trigger, a more reliable alternative for such case, is to use the '
        'multi-frame mode.\n\n')
    if CHOSEN_TRIGGER == TriggerType.SOFTWARE:
        print('Software trigger chosen ...')
    elif CHOSEN_TRIGGER == TriggerType.HARDWARE:
        print('Hardware trigger chose ...')

    try:
        # Ensure trigger mode off
        # The trigger must be disabled in order to configure whether the source
        # is software or hardware.
        nodemap = cam.GetNodeMap()
        node_trigger_mode = PySpin.CEnumerationPtr(nodemap.GetNode('TriggerMode'))
        if not PySpin.IsAvailable(node_trigger_mode) or not PySpin.IsReadable(node_trigger_mode):
            print('Unable to disable trigger mode (node retrieval). Aborting...')
            return False

        node_trigger_mode_off = node_trigger_mode.GetEntryByName('Off')
        if not PySpin.IsAvailable(node_trigger_mode_off) or not PySpin.IsReadable(node_trigger_mode_off):
            print('Unable to disable trigger mode (enum entry retrieval). Aborting...')
            return False

        node_trigger_mode.SetIntValue(node_trigger_mode_off.GetValue())

        print('Trigger mode disabled...')

        # Set TriggerSelector to FrameStart
        # For this example, the trigger selector should be set to frame start.
        # This is the default for most cameras.
        node_trigger_selector = PySpin.CEnumerationPtr(nodemap.GetNode('TriggerSelector'))
        if not PySpin.IsAvailable(node_trigger_selector) or not PySpin.IsWritable(node_trigger_selector):
            print('Unable to get trigger selector (node retrieval). Aborting...')
            return False

        node_trigger_selector_framestart = node_trigger_selector.GetEntryByName('FrameStart')
        if not PySpin.IsAvailable(node_trigger_selector_framestart) or not PySpin.IsReadable(
                node_trigger_selector_framestart):
            print('Unable to set trigger selector (enum entry retrieval). Aborting...')
            return False
        node_trigger_selector.SetIntValue(node_trigger_selector_framestart.GetValue())

        print('Trigger selector set to frame start...')

        # Select trigger source
        # The trigger source must be set to hardware or software while trigger
        # mode is off.
        node_trigger_source = PySpin.CEnumerationPtr(nodemap.GetNode('TriggerSource'))
        if not PySpin.IsAvailable(node_trigger_source) or not PySpin.IsWritable(node_trigger_source):
            print('Unable to get trigger source (node retrieval). Aborting...')
            return False

        if CHOSEN_TRIGGER == TriggerType.SOFTWARE:
            node_trigger_source_software = node_trigger_source.GetEntryByName('Software')
            if not PySpin.IsAvailable(node_trigger_source_software) or not PySpin.IsReadable(
                    node_trigger_source_software):
                print('Unable to set trigger source (enum entry retrieval). Aborting...')
                return False
            node_trigger_source.SetIntValue(node_trigger_source_software.GetValue())
            print('Trigger source set to software...')

        elif CHOSEN_TRIGGER == TriggerType.HARDWARE:
            node_trigger_source_hardware = node_trigger_source.GetEntryByName('Line0')
            if not PySpin.IsAvailable(node_trigger_source_hardware) or not PySpin.IsReadable(
                    node_trigger_source_hardware):
                print('Unable to set trigger source (enum entry retrieval). Aborting...')
                return False
            node_trigger_source.SetIntValue(node_trigger_source_hardware.GetValue())
            print('Trigger source set to hardware...')

        # Turn trigger mode on
        # Once the appropriate trigger source has been set, turn trigger mode
        # on in order to retrieve images using the trigger.
        node_trigger_mode_on = node_trigger_mode.GetEntryByName('On')
        if not PySpin.IsAvailable(node_trigger_mode_on) or not PySpin.IsReadable(node_trigger_mode_on):
            print('Unable to enable trigger mode (enum entry retrieval). Aborting...')
            return False

        node_trigger_mode.SetIntValue(node_trigger_mode_on.GetValue())
        print('Trigger mode turned back on...')

    except PySpin.SpinnakerException as ex:
        print('Error: %s' % ex)
        return False

    return result

# From Spinnaker SDK : Examples : (copyright) FLIR
def grab_next_image_by_trigger(nodemap):
    """
    This function acquires an image by executing the trigger node.

    :param cam: Camera to acquire images from.
    :param nodemap: Device nodemap.
    :type cam: CameraPtr
    :type nodemap: INodeMap
    :return: True if successful, False otherwise.
    :rtype: bool
    """
    try:
        result = True
        # Use trigger to capture image
        # The software trigger only feigns being executed by the Enter key;
        # what might not be immediately apparent is that there is not a
        # continuous stream of images being captured; in other examples that
        # acquire images, the camera captures a continuous stream of images.
        # When an image is retrieved, it is plucked from the stream.

        if CHOSEN_TRIGGER == TriggerType.SOFTWARE:
            # Get user input, no need.
            # input('Press the Enter key to initiate software trigger.')

            # Execute software trigger
            node_softwaretrigger_cmd = PySpin.CCommandPtr(nodemap.GetNode('TriggerSoftware'))
            if not PySpin.IsAvailable(node_softwaretrigger_cmd) or not PySpin.IsWritable(node_softwaretrigger_cmd):
                print('Unable to execute trigger. Aborting...')
                return False

            node_softwaretrigger_cmd.Execute()
            time.sleep(2) # Implemented the sleep command for that two second delay.


        elif CHOSEN_TRIGGER == TriggerType.HARDWARE:
            print('Use the hardware to trigger image acquisition.')

    except PySpin.SpinnakerException as ex:
        print('Error: %s' % ex)
        return False

    return result

# From Spinnaker SDK : Examples : (copyright) FLIR
def acquire_images(cam, nodemap, nodemap_tldevice):
    """
    This function acquires and saves _5_ images from a device.
    This has been modified to acquire images after the camera has reached a certain tempertature. 

    :param cam: Camera to acquire images from.
    :param nodemap: Device nodemap.
    :param nodemap_tldevice: Transport layer device nodemap.
    :type cam: CameraPtr
    :type nodemap: INodeMap
    :type nodemap_tldevice: INodeMap
    :return: True if successful, False otherwise.
    :rtype: bool
    """
    # Configurs the text file for image numbering
    Accuracy = open("Accuracy.json", "r")
    load = json.load(Accuracy)
    image_num_config = int(load["NumPhotos"])
    Accuracy.close()

    Accuracy = open("Accuracy.json", "w")
    load["NumPhotos"] = int(load["NumPhotos"]) + NUM_IMAGES
    json.dump(load, Accuracy)


    

    print('*** IMAGE ACQUISITION ***\n')
    try:
        result = True

        # Set acquisition mode to continuous
        # In order to access the node entries, they have to be casted to a pointer type (CEnumerationPtr here)
        node_acquisition_mode = PySpin.CEnumerationPtr(nodemap.GetNode('AcquisitionMode'))
        if not PySpin.IsAvailable(node_acquisition_mode) or not PySpin.IsWritable(node_acquisition_mode):
            return False

        # Retrieve entry node from enumeration node
        node_acquisition_mode_continuous = node_acquisition_mode.GetEntryByName('Continuous')
        if not PySpin.IsAvailable(node_acquisition_mode_continuous) or not PySpin.IsReadable(
                node_acquisition_mode_continuous):
            print('Unable to set acquisition mode to continuous (entry retrieval). Aborting...')
            return False

        # Change to RGB rather than Mono 8
        if cam.PixelFormat.GetAccessMode() == PySpin.RW:
            cam.PixelFormat.SetValue(PySpin.PixelFormat_BayerRG8)

        # TODO : Is not legit | This is for tonight. 
        # node_pixel_format = PySpin.CEnumerationPtr(nodemap.GetNode('PixelFormat'))
        # if not PySpin.IsAvailable(node_pixel_format) or not PySpin.IsReadable(
        #        node_pixel_format):
        #     return False
        # pixel_format_BayerBGR8 = PySpin.CEnumEntryPtr(node_pixel_format.GetEntryByName('BGR8'))
        # node_pixel_format.SetIntValue(pixel_format_BayerBGR8)

        # Retrieve integer value from entry node
        acquisition_mode_continuous = node_acquisition_mode_continuous.GetValue()

        # Set integer value from entry node as new value of enumeration node
        node_acquisition_mode.SetIntValue(acquisition_mode_continuous)

        # print('Acquisition mode set to continuous...')

        #  Begin acquiring images
        cam.BeginAcquisition()

        print('Acquiring images...')
        device_serial_number = ''
        node_device_serial_number = PySpin.CStringPtr(nodemap_tldevice.GetNode('DeviceSerialNumber'))
        if PySpin.IsAvailable(node_device_serial_number) and PySpin.IsReadable(node_device_serial_number):
            device_serial_number = node_device_serial_number.GetValue()
            # print('Device serial number retrieved as %s...' % device_serial_number)

        # Retrieve, convert, and save images
        for i in range(NUM_IMAGES):
            try:
                #  Retrieve the next image from the trigger
                result &= grab_next_image_by_trigger(nodemap)

                #  Retrieve next received image
                image_result = cam.GetNextImage(1000)

                #  Ensure image completion
                if image_result.IsIncomplete():
                    print('Image incomplete with image status %d ...' % image_result.GetImageStatus())

                else:

                    # Create a unique filename
                    if device_serial_number:
                        filename = 'sample-%s-%d-%d.raw' % (device_serial_number, i +
                                                            image_num_config, GetCameraTemperature(cam))
                    else:  # if serial number is empty
                         filename = 'sample-%s-%d.raw' % (i +
                                                            image_num_config, GetCameraTemperature(cam))

                    # Save image
                    #  *** NOTES ***
                    #  The standard practice of the examples is to use device
                    #  serial numbers to keep images of one device from
                    #  overwriting those of another.
                    image_result.Save(filename)
                    print('Image saved at %s\n' % filename)

                    #  Release image
                    #
                    #  *** NOTES ***
                    #  Images retrieved directly from the camera (i.e. non-converted
                    #  images) need to be released in order to keep from filling the
                    #  buffer.
                    image_result.Release()

            except PySpin.SpinnakerException as ex:
                print('Error: %s' % ex)
                return False

            time.sleep(2)

        # End acquisition
        #
        #  *** NOTES ***
        #  Ending acquisition appropriately helps ensure that devices clean up
        #  properly and do not need to be power-cycled to maintain integrity.
        cam.EndAcquisition()

    except PySpin.SpinnakerException as ex:
        print('Error: %s' % ex)
        return False

    return result

# From Spinnaker SDK : Examples : (copyright) FLIR
def reset_trigger(nodemap):
    """
    This function returns the camera to a normal state by turning off trigger mode.

    :param nodemap: Transport layer device nodemap.
    :type nodemap: INodeMap
    :returns: True if successful, False otherwise.
    :rtype: bool
    """
    try:
        result = True
        node_trigger_mode = PySpin.CEnumerationPtr(nodemap.GetNode('TriggerMode'))
        if not PySpin.IsAvailable(node_trigger_mode) or not PySpin.IsReadable(node_trigger_mode):
            print('Unable to disable trigger mode (node retrieval). Aborting...')
            return False

        node_trigger_mode_off = node_trigger_mode.GetEntryByName('Off')
        if not PySpin.IsAvailable(node_trigger_mode_off) or not PySpin.IsReadable(node_trigger_mode_off):
            print('Unable to disable trigger mode (enum entry retrieval). Aborting...')
            return False

        node_trigger_mode.SetIntValue(node_trigger_mode_off.GetValue())
    
        print('Trigger mode disabled...')

    except PySpin.SpinnakerException as ex:
        # print('Error: %s' % ex)
        result = False

    return result

# Auto Expose Images Between each image. 
def AutoExposure(cam):
    if cam.ExposureAuto.GetAccessMode() == PySpin.RW:
        cam.ExposureAuto.SetValue(PySpin.ExposureAuto_Continuous)
        return True
    return False

# as they are not issues in the origional script.  
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
        err = False

        # Retrieve TL device nodemap and print device information
        nodemap_tldevice = cam.GetTLDeviceNodeMap()
        cam.Init()
        # Retrieve GenICam nodemap
        nodemap = cam.GetNodeMap()

        # Configure trigger
        if configure_trigger(cam) is False:
            return False

        result&= Heat(cam,temp)

        result &= AutoExposure(cam)

        # Acquire images
        result &= acquire_images(cam, nodemap, nodemap_tldevice)

        # Reset trigger
        result &= reset_trigger(nodemap)
        
        cam.DeInit()

    except PySpin.SpinnakerException as ex:
        # print('Error: %s' % ex)
        result = False

    return result

def GetCameraTemperature(cam):
    if cam.DeviceTemperature.GetAccessMode() == PySpin.RO:
        return float(cam.DeviceTemperature.ToString())

def BarProg(TempNext,Temp):
    if(TempNext > Temp):
        return TempNext-Temp
    return 0

# Does the temperature sensing during the loops.
def Heat(cam, GoalTemperature):
    # Get Temperature of Camera
    Temp = GetCameraTemperature(cam)
    # Heating
    asyncio.run(HeatGun.On()) 
    """
        Continue Heating unitl goal temperature is achieved
    """
    TempBar = Bar('Heating',fill='█',index=Temp,max=GoalTemperature)
    while Temp < GoalTemperature:
        Temp = GetCameraTemperature(cam)
        time.sleep(5)
        TempBar.index = GetCameraTemperature(cam)
        TempBar.next(BarProg(GetCameraTemperature(cam),Temp))
    TempBar.finish()

    # Capture 1 image
    print('Heating Paused\n')
    if Temp >= GoalTemperature:
        """
        about: Discontinue Heating when goal temperature is achieved
        """
        asyncio.run(HeatGun.Off())
        print("Heating Paused")
        return True
       

# Bootstrap
def main(argv):
    print("This is a heavily modified version of FLIR Teledyne's Triggery.py Script that is being used under the Alias HeatTrigger.py\n") 
    system = PySpin.System.GetInstance()

    # Retrieve list of cameras from the system
    cam_list = system.GetCameras()

    num_cameras = cam_list.GetSize()

    # From Spinnaker SDK Examples
    if num_cameras == 0:
        # Clear camera list before releasing system
        cam_list.Clear()

        # Release system instance
        system.ReleaseInstance()
        print("\n")
        print('Zero Cameras Discovered.\n')
        return False

    # List of Cameras, loop seems like a bad idea, perhaps argv? 
    """
        Takes cmdln args, and heats camera to specified temperature, more reliable than loop. 
    """
    for i, cam in enumerate(cam_list):
        try: 
            Capture(cam,int(argv))
        except PySpin.SpinnakerException as ex:
            break
    del cam # It's about the little things in programming...
    print('Capture Completed...')
    # Clear camera list before releasing system, this makes a mess if not cleared
    cam_list.Clear()

    # Release system instance
    system.ReleaseInstance()

if __name__ == '__main__':
    if main(sys.argv[1]):
        sys.exit(0)
    else:
        sys.exit(1)