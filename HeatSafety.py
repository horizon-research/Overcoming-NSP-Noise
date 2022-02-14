import PySpin
import sys
import time
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
    cam.Init()
    print('Please cool the camera, it is currently: %s' % GetCameraTemperature(cam))
    cam.DeInit()


def Capture(cam, GoalTemperature):
    # Get Temperature of Camera

    Temp = GetCameraTemperature(cam)
    print(GoalTemperature)

    # Heating
    while Temp < GoalTemperature:
        cam.Init()
        Temp = GetCameraTemperature(cam)
        print(Temp)
        time.sleep(3)

    # Capture 10 images
    if Temp > GoalTemperature:
        # cam.DeInit()
        print("Capturing, please stop heating")
        Trigger.run_single_camera(cam)  # Cites : FLIR TELEDYNE




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
        print('Oops, Camera(s) not detected, please check your connection and try again.')
        print("\n")
        return False

    # gets the camera temperature.
    for i, cam in enumerate(cam_list):
        for t in range(40, 42, 1):
            # Initiates Capture
            Capture(cam, t)
            time.sleep(1)

    print("Capture Complete, please cool the camera.")
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
