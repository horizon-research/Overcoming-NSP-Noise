import PySpin

# PseudoCode

SafeTemperature = 40  # Must be reached after each test
CameraTemp = PySpin.Camera.DeviceTemperature


def RunningScript(temperature):
    while PySpin.Camera.DeviceTemperature < temperature:
        Heat(temperature)

    PySpin.Camera.Init()
    PySpin.Camera.DeviceTemperatureSelector

    if PySpin.Camera.DeviceTemperature == temperature:
        Capture(temperature)


def CoolToSafety():
    while PySpin.Camera.DeviceTemperature > 50:
        print("Cooling the Camera to", SafeTemperature, "°C")
        # Fan().Blow()
        # print("Heat gun off")


def Capture(temperature):
    print("Capturing 10 x images at: ", temperature, "°C")


def Heat(temperature):
    print("Heating to", temperature, end="\n")

    # While(Temperature < Goal Temp)
    # Fans().Off
    # Print("Heat gun on low")


def main():
    # Temp Array = ArrayofTemperature() (from 50 -> 80 C)
    TempArray = []  # Fill the array of temperatures to test the camera on.

    for i in range(50, 85, 5):
        TempArray.append(i)

    # Run the Running Script
    for i in TempArray:
        RunningScript(i)
        CoolToSafety()
        print("\n")


if __name__ == "__main__":
    main()
