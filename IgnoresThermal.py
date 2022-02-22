# This will be the Neural Network Script
# Honestly, the most important part is deciding what in the world you are imaging.
# Otherwise, how in the world can you tailor the needs of the NN.

# TODO LIST
#  input - Images from camera : Import a folder of those images.
#  Design a CNN that makes use of max-pooling.

# TODO : today
# import working file scanner that reads in each image file.

# What could be interesting?
    # Is a starbucks drink mine? Looking for my name on cups of Starbucks coffee.
    # Noise will be inducedf
import pathlib


def main() :
    print("\n")

    for path in pathlib.Path("Training_Data/Refresh").iterdir():
        if path.is_file():
            current_file = open(path, "r")
            print(current_file.name)
            current_file.close()

    print("\n")

    for path in pathlib.Path("Training_Data/BOSE").iterdir():
        if path.is_file():
            current_file = open(path, "r")
            print(current_file.name)
            current_file.close()

    print("\n")

    for path in pathlib.Path("Training_Data/WhiteCup").iterdir():
        if path.is_file():
            current_file = open(path, "r")
            print(current_file.name)
            current_file.close()

    print("\n")

if __name__ == '__main__':
    main()





