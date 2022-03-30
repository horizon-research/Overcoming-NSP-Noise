# This will be the Neural Network Script
# Cites : https://keras.io/examples/vision/image_classification_from_scratch/
# Cites : https://www.tensorflow.org/tutorials/images/cnn
# Depends on : pydot and Graphviz

import tensorflow as tf
import json
from tensorflow import keras
from tensorflow.keras import layers

# Reduced batch size to lower the CPU load and to accelerate the processing
image_size = (200, 200)
batch_size = 5 

# Creates the DataSet for training from the hot and iced coffee images
DataSet = tf.keras.preprocessing.image_dataset_from_directory(
    "Training_Data",
    validation_split=0.2,
    subset="training",
    seed=1337,
    image_size=image_size,
    batch_size=batch_size,
)
# Creates the DataSet for training from the iced and hot coffee images
Validation = tf.keras.preprocessing.image_dataset_from_directory(
    "Training_Data",
    validation_split=0.2,
    subset="validation",
    seed=1337,
    image_size=image_size,
    batch_size=batch_size,
)


# This is a method useful for our use-case where I doubt I can
# capture a data set of 10,000, but 464 will do for now.
# This does not modify the pixels but merely stretches them and
data_augmentation = keras.Sequential(
    [layers.RandomFlip("horizontal"), layers.RandomRotation(0.1), layers.RandomRotation(0.6),
     layers.RandomFlip("vertical") , layers.RandomZoom(0.3), layers.RandomContrast(0.7),
     layers.RandomContrast(0.1)]
)

# Prevents I/O issues
train_ds = DataSet.prefetch(buffer_size=32)
val_ds = Validation.prefetch(buffer_size=32)


def SixtyFour(x):
    for i in range(0,3):
        x = layers.Activation("sigmoid")(x)
        x = layers.Conv2D(64, 3, strides=2, padding="same")(x)
        x = layers.BatchNormalization()(x)
        previous_block_activation = x 
        residual = layers.Conv2D(64, 3, strides=2, padding="same")(
            previous_block_activation
        )
        x = layers.Activation("sigmoid")(x)
        x = layers.Conv2D(64, 3, strides=2, padding="same")(x)
        x = layers.BatchNormalization()(x)
        x = layers.add([x, residual])  # Add back residual
        previous_block_activation = x 
        x = layers.Dropout(0.3)(x)

    return x     

def OneTwentyEight(x):
    for i in range(0,4):
        x = layers.Activation("sigmoid")(x)
        x = layers.Conv2D(128, 3, strides=2, padding="same")(x)
        x = layers.BatchNormalization()(x)
        x = layers.Dropout(0.3)(x)
        previous_block_activation = x 
        residual = layers.Conv2D(128, 3, strides=2, padding="same")(
            previous_block_activation
        )
        x = layers.Activation("sigmoid")(x)
        x = layers.Conv2D(128, 3, strides=2, padding="same")(x)
        x = layers.BatchNormalization()(x)
        x = layers.Dropout(0.3)(x) 
        x = layers.add([x, residual])  # Add back residual
        previous_block_activation = x 
    return x            

def TwoFiftySix(x):
    for i in range(0,6):
        x = layers.Activation("sigmoid")(x)
        x = layers.Conv2D(256, 3, strides=2, padding="same")(x)
        x = layers.BatchNormalization()(x)
        previous_block_activation = x 
        residual = layers.Conv2D(256, 3, strides=2, padding="same")(
            previous_block_activation
        )
        x = layers.Activation("sigmoid")(x)
        x = layers.Conv2D(256, 3, strides=2, padding="same")(x)
        x = layers.BatchNormalization()(x)
        x = layers.add([x, residual])  # Add back residual
        previous_block_activation = x        
    return x         

def FiveTwelve(x):
    for i in range(0,3):
        x = layers.Activation("sigmoid")(x)
        x = layers.Conv2D(512, 3, strides=2, padding="same")(x)
        x = layers.BatchNormalization()(x)
        previous_block_activation = x 
        residual = layers.Conv2D(512, 3, strides=2, padding="same")(
            previous_block_activation
        )
        x = layers.Activation("sigmoid")(x)
        x = layers.Conv2D(512, 3, strides=2, padding="same")(x)
        x = layers.BatchNormalization()(x)
        x = layers.add([x, residual])  # Add back residual
        previous_block_activation = x    
    return x                


# Cites this Model as a sample : https://keras.io/examples/vision/image_classification_from_scratch/
# Directly Cites : https://keras.io/examples/vision/image_classification_from_scratch/
def NModel(input_shape, num_classes):
    inputs = keras.Input(shape=input_shape)
    # Image augmentation block
    # Entry block
    """
    This is a modified ResNet Model
    """
    x = data_augmentation(inputs)
    x = layers.Rescaling(1.0 / 255)(x)
    x = FiveTwelve(
        TwoFiftySix(
            OneTwentyEight
            (SixtyFour(x)
            )
        )
    )
    x = layers.Dropout(0.1)(x)
    x = FiveTwelve(
        TwoFiftySix(
            OneTwentyEight
            (SixtyFour(x)
            )
        )
    )
    x = layers.Dropout(0.1)(x)
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


def Compile():
    model = NModel(input_shape=image_size + (3,), num_classes=2)
    keras.utils.plot_model(model, show_shapes=True)
    epochs = 1  # over-fitting?
    callbacks = [keras.callbacks.ModelCheckpoint("IgnoresThermal_{epoch}.h5"), ]
    model.compile(
        optimizer=keras.optimizers.SGD(0.01),
        loss="binary_crossentropy",
        metrics=["accuracy"]
    )

    model.fit(DataSet, shuffle=True,
              epochs=epochs, callbacks=callbacks, validation_data=Validation
              )


def Test(image):
    model = NModel(input_shape=image_size + (3,), num_classes=2)
    img = keras.preprocessing.image.load_img(
        image, target_size=image_size
    )
    img_array = keras.preprocessing.image.img_to_array(img)
    img_array = tf.expand_dims(img_array, 0)  # Create batch axis
    predictions = model.predict(img_array)
    score = predictions[0]

    print("This image is %.2f percent hot coffee and this image is %.2f percent iced coffee." % (
        100 * score, 100 * (1 - score)))

    if 100 * score > (100 * (1 - score)) and 100 * score > 0.55:
        print("This image is hot coffee\n")
        return True  # Hot coffee is true
    elif 100 * score < (100 * (1 - score)) and (100 * (1 - score)) > 0.55:
        print("This image is cold coffee\n")
        return False  # Cold coffee is false
    else:
        print("This image is niether hot nor cold coffee")
        return -1


def Statistics(img1, img2, img3, img4):
    Accuracy = open("Accuracy.json", "r")
    load = json.load(Accuracy)
    Acc = load['Accuracy'] * load['Trials']
    print("Current accuracy is %f: " % load['Accuracy'])
    Nt = load['Trials'] + 4
    Accuracy.close()
    A = 0
    print("You have selected test")
    print("Images of hot coffee")
    T1 = Test(img1)  # This image is incredibly interesting because it has cold features but is hot.
    if T1:
        A += 1
    T2 = Test(img2)
    if T2:
        A += 1
    print("Images of iced coffee")
    T3 = Test(img3)
    if not T3:
        A += 1
    T4 = Test(img4)
    if not T4:
        A += 1
    Acc = (A + Acc) / Nt
    Accuracy = open("Accuracy.json", "w")
    load["Accuracy"] = Acc
    load["Trials"] = load["Trials"] + A
    print("Current final accuracy is %f: " % Acc)
    json.dump(load, Accuracy)
    Accuracy.close()


def main():
    print("\nWelcome to Hot or Iced Coffee")
    x = input("\
    \n - Please enter \'1\' for compile, \'2\' for test, or \'3\' for both.\
    \n\n - You may also press \'c\' for the current accuracy\n")

    if x == "1":
        print("You have selected compile")
        Compile()

    elif x == "2":
        Statistics('HotCupUnderKeurig.jpeg', 'ACup.JPG', 'TesterCold.jpeg', "ICED5x.jpg")

    elif x == "3":
        print("You have selected to compile and test")
        Compile()
        Statistics('HotCupUnderKeurig.jpeg', 'ACup.JPG', 'TesterCold.jpeg', "ICED5x.jpg")
    
    elif x == "c": #  Current Accuracy
        Accuracy = open("Accuracy.json", "r")
        load = json.load(Accuracy)
        Accuracy.close()
        Acc = load['Accuracy'] * 100
        Acc = round(Acc,3)
        out = ("The current accuracy {Acc} %").format(Acc = Acc)
        print(out)

if __name__ == '__main__':
    main()
