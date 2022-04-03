# This is the driver script for the experimentation with the FLIR BLACKFLY S Camera
# This script relies on the Trigger.py script provided Copyright (c) 2001-2021 FLIR Systems, Inc. All Rights Reserved.
#
# Essentially this script is a temperature trigger for the camera that continues running until all captures are taken
# =============================================================================
import json
import PySpin
import sys
import time
import Trigger as t
# Take two images per click.


# My Additions to this script:
# Grabs the temperature of the camera, returns it as a float
def GetCameraTemperature(cam):
    x = 0
    if cam.DeviceTemperature.GetAccessMode() == PySpin.RO:
        x = cam.DeviceTemperature.ToString()
    x = float(x)

    return x


# Does the temperature sensing during the loops.
def Go(cam, GoalTemperature):
    # Get Temperature of Camera

    Temp = GetCameraTemperature(cam)
    print(GoalTemperature)

    # Heating
    while Temp < GoalTemperature:
        Temp = GetCameraTemperature(cam)
        print("Camera is currently", Temp, "°C")
        time.sleep(5)  # Protects the camera.

    # Capture 1 image
    if Temp >= GoalTemperature:
        print("Capturing, please continue heating")
        t.run_single_camera(cam)  # Cites : FLIR TELEDYNE


# Bootstrap
def main():
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
        print('Camera(s) not detected, please check your connection and try again.')
        print("\n")
        return False

    # List of Cameras
    for i, cam in enumerate(cam_list):
        # List of Temperatures
        for t in range(70, 95, 1):
            # Initiates Capture
            cam.Init()
            Go(cam, t)
            time.sleep(2)

    print("Capture Complete, please cool the camera.")
    print("Please do not touch the camera, it is most likely 50°C+.")

    # Clear camera list before releasing system, this makes a mess if not cleared
    cam_list.Clear()

    # Release system instance
    system.ReleaseInstance()


if __name__ == '__main__':
    if main():
        sys.exit(0)
    else:
        sys.exit(1)
