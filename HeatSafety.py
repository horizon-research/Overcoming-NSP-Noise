import PySpin
import sys
import os
import Trigger  # This doesn't quite work the way I need it to, it is a stand in for trigger code that will be added

cameraTemperature = 0
NUM_IMAGES = 10  # number of images to grab


# Grabs the temperature of the camera, returns it as a float
def GetCameraTemperature(cam):
    x = 0
    if cam.DeviceTemperature.GetAccessMode() == PySpin.RO:
        x = cam.DeviceTemperature.ToString()

    x = float(x)
    return x


def Cool(cam):
    print('Please cool the camera, it is currently: %s' % GetCameraTemperature(cam))


def HeatSafety(cam, GoalTemperature):
    Temp = GetCameraTemperature(cam)
    print(GoalTemperature)
    nodeMap = cam.GetNodeMap()
    while Temp < GoalTemperature:
        Temp = GetCameraTemperature(cam)
        print("Heating")

    if Temp > GoalTemperature:
        print("Capturing, please stop heating")
        Trigger.run_single_camera(cam)  # Cites : FLIR TELEDYNE
    Cool(cam)


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

        print('Not enough cameras!')
        input('Done! Press Enter to exit...')
        return False

    # gets the camera temperature.
    # for x in range(40, 85, 5):
    for i, cam in enumerate(cam_list):
        cam.Init()
        HeatSafety(cam, 34)

    del cam

    # Clear camera list before releasing system, this makes a mess if not cleared
    cam_list.Clear()

    # Release system instance
    system.ReleaseInstance()


if __name__ == '__main__':
    if main():
        sys.exit(0)
    else:
        sys.exit(1)
