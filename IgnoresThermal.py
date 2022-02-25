# This will be the Neural Network Script
# Cites : https://keras.io/examples/vision/image_classification_from_scratch/
# Cites : https://www.tensorflow.org/tutorials/images/cnn
# Depends on : pydot and Graphviz
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers



image_size = (100, 100) #More power needed, but more accuracy gained.
batch_size = 32

DataSet = tf.keras.preprocessing.image_dataset_from_directory(
    "Training_Data",
    validation_split=0.2,
    subset="training",
    seed=1337,
    image_size=image_size,
    batch_size=batch_size,
)

Validation = tf.keras.preprocessing.image_dataset_from_directory(
    "Training_Data",
    validation_split=0.1,
    subset="validation",
    seed=1337,
    image_size=image_size,
    batch_size=batch_size,
)

# This is a method useful for our use-case where I doubt I can
# capture a data set of 10,000.
data_augmentation = keras.Sequential(
    [layers.RandomFlip("horizontal"),
     layers.RandomRotation(0.1),
     layers.RandomFlip("vertical"),
     ]
)


# # For CPU training
augmented_train_ds = DataSet.map(
    lambda x, y: (data_augmentation(x, training=True), y)
)


# Prevents I/O issues
train_ds = DataSet.prefetch(buffer_size=32)
val_ds = Validation.prefetch(buffer_size=32)


# Directly Cites : https://keras.io/examples/vision/image_classification_from_scratch/
def NModel(input_shape, num_classes):
    inputs = keras.Input(shape=input_shape)
    x = data_augmentation(inputs)
    x = layers.Rescaling(1.0 / 255)(x)
    x = layers.SeparableConv2D(128, 3, padding="same")(x)

    previous_block_activation = x

    for size in [128, 256, 512, 1024]:
        x = layers.Activation("relu")(x)
        x = layers.SeparableConv2D(size, 3, padding="same")(x)
        x = layers.BatchNormalization()(x)

        x = layers.MaxPooling2D(3, strides=2, padding="same")(x)  # Key for noisy images, use more than once?

        residual = layers.Conv2D(size, 1, strides=2, padding="same")(
            previous_block_activation
        )
        x = layers.add([x, residual])
        previous_block_activation = x

        x = layers.Activation("tanh")(x)
        x = layers.SeparableConv2D(size, 3, padding="same")(x)
        x = layers.BatchNormalization()(x)

        x = layers.MaxPooling2D(3, strides=2, padding="same")(x)  # Key for noisy images, use more than once?

        residual = layers.Conv2D(size, 1, strides=2, padding="same")(
            previous_block_activation
        )
        x = layers.add([x, residual])

        previous_block_activation = x

        x = layers.Activation("tanh")(x)
        x = layers.SeparableConv2D(size, 3, padding="same")(x)
        x = layers.BatchNormalization()(x)

        x = layers.MaxPooling2D(3, strides=2, padding="same")(x)  # Key for noisy images, use more than once?

        residual = layers.Conv2D(size, 1, strides=2, padding="same")(
            previous_block_activation
        )
        x = layers.add([x, residual])
        previous_block_activation = x

        x = layers.MaxPooling2D(3, strides=2, padding="same")(x)  # Key for noisy images, use more than once?

        residual = layers.Conv2D(size, 1, strides=2, padding="same")(
            previous_block_activation
        )
        x = layers.add([x, residual])
        previous_block_activation = x



    # TODO : Look up for comprehension
    x = layers.SeparableConv2D(128, 3, padding="same")(x)
    x = layers.BatchNormalization()(x)
    x = layers.Activation("relu")(x)

    x = layers.GlobalAveragePooling2D()(x)
    if num_classes == 2:
        activation = "sigmoid"
        units = 1
    else:
        activation = "sigmoid"
        units = num_classes

    x = layers.Dropout(0.5)(x)
    outputs = layers.Dense(units, activation=activation)(x)
    return keras.Model(inputs, outputs)


model = NModel(input_shape=image_size + (3,), num_classes=2)

def Compile() :
    keras.utils.plot_model(model, show_shapes=True)
    epochs = 10 # over-fitting?
    callbacks = [keras.callbacks.ModelCheckpoint("save_at_{epoch}.h5"), ]
    model.compile(
        optimizer=keras.optimizers.SGD(1e-3),
        loss="binary_crossentropy",
        metrics=["accuracy"],
    )
    model.fit(DataSet, epochs=epochs, callbacks=callbacks, validation_data=Validation)

def Test(image):
    img = keras.preprocessing.image.load_img(
        image, target_size=image_size
        # Test image is of a coffee cup with my name on it from fall of 2020.
    )
    img_array = keras.preprocessing.image.img_to_array(img)
    img_array = tf.expand_dims(img_array, 0)  # Create batch axis
    predictions = model.predict(img_array)
    score = predictions[0]
    print("This image is %.2f percent your coffee." % (100 * (score)))


def main():
    x = input("Please Enter 1 for compile 2 for test and 3 for both\n")
    if(x == "1"):
        Compile()
    elif(x == "2"):
        print("Image of my coffee")
        Test("Training_Data/sample-18255214-481-28.png")
    elif(x == "3"):
        Compile()
        Test("Training_Data/Test.png")

if __name__ == '__main__':
    main()