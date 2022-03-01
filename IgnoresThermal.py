# This will be the Neural Network Script
# Cites : https://keras.io/examples/vision/image_classification_from_scratch/
# Cites : https://www.tensorflow.org/tutorials/images/cnn
# Depends on : pydot and Graphviz
import tensorflow as tf
from matplotlib import pyplot as plt
from tensorflow import keras
from tensorflow.keras import layers
import matplotlib.pyplot as plt

# Reduced batch size to lower the CPU load and to accelerate the processing
image_size = (1200, 1200)
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
    [layers.RandomFlip("horizontal"), layers.RandomRotation(0.1),
     layers.RandomFlip("vertical")]
)

# Prevents I/O issues
train_ds = DataSet.prefetch(buffer_size=32)
val_ds = Validation.prefetch(buffer_size=32)


# Directly Cites : https://keras.io/examples/vision/image_classification_from_scratch/
def NModel(input_shape, num_classes):
    inputs = keras.Input(shape=input_shape)
    # Image augmentation block
    x = data_augmentation(inputs)

    # Entry block
    x = layers.Rescaling(1.0 / 255)(x)
    x = layers.Conv2D(128, 3, strides=2, padding="same")(x)
    x = layers.BatchNormalization()(x)
    x = layers.Activation("softmax")(x)

    x = layers.Conv2D(1024, 3, padding="same")(x)
    x = layers.BatchNormalization()(x)
    x = layers.Activation("softmax")(x)

    previous_block_activation = x  # Set aside residual

    for size in [128, 256, 512, 728]:
        x = layers.Activation("elu")(x)
        x = layers.SeparableConv2D(size, 3, padding="same")(x)
        x = layers.BatchNormalization()(x)

        x = layers.Activation("softmax")(x)
        x = layers.SeparableConv2D(size, 3, padding="same")(x)
        x = layers.BatchNormalization()(x)

        x = layers.MaxPooling2D(3, strides=2, padding="same")(x)

        # Project residual
        residual = layers.Conv2D(size, 1, strides=2, padding="same")(
            previous_block_activation
        )
        x = layers.add([x, residual])  # Add back residual
        previous_block_activation = x  # Set aside next residual

    x = layers.SeparableConv2D(1024, 3, padding="same")(x)
    x = layers.BatchNormalization()(x)
    x = layers.Activation("elu")(x)

    x = layers.GlobalAveragePooling2D()(x)
    if num_classes == 2:
        activation = "softmax"
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
    callbacks = [keras.callbacks.ModelCheckpoint("save_at_{epoch}.h5"), ]
    model.compile(
        optimizer=keras.optimizers.SGD(1e-3),
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
        # Test image is of a coffee cup with my name on it from fall of 2020.
    )
    img_array = keras.preprocessing.image.img_to_array(img)
    img_array = tf.expand_dims(img_array, 0)  # Create batch axis
    predictions = model.predict(img_array)
    score = predictions[0]
    print("This image is %.2f percent hot coffee and this image is %.2f percent iced coffee." % (
        100 * score, (100 * (1 - score))))


def main():
    x = input("Please Enter 1 for compile 2 for test and 3 for both\n")

    if x == "1":
        print("You have selected compile")
        Compile()

    elif x == "2":
        print("You have selected test")
        print("Images of hot coffee")
        Test("HOT.JPG")
        Test("HOT2.jpeg")
        print("Images of iced coffee")
        Test("ICED.jpeg")
        Test("A.jpg")

    elif x == "3":
        print("You have selected to compile and test")
        Compile()
        print("Images of hot coffee")
        Test("HOT.JPG")
        Test("HOT2.jpeg")
        print("Images of iced coffee")
        Test("ICED.jpeg")
        Test("ICED2.jpeg")


if __name__ == '__main__':
    main()
