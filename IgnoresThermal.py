# This will be the Neural Network Script
# Cites : https://keras.io/examples/vision/image_classification_from_scratch/
# Depends on : pydot and Graphviz
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers

images = [] # DataSet of Images

image_size = (180, 180)
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
    validation_split=0.2,
    subset="validation",
    seed=1337,
    image_size=image_size,
    batch_size=batch_size,
)

# This is a method useful for our use-case where I doubt I can
# capture a data set of 10,000.
data_augmentation = keras.Sequential(
    [ layers.RandomFlip("horizontal"),
      layers.RandomRotation(0.1)
    ]
)

# For CPU training
augmented_train_ds = DataSet.map(
  lambda x, y: (data_augmentation(x, training=True), y)
)

# Prevents I/O issues
train_ds = DataSet.prefetch(buffer_size=32)
val_ds = Validation.prefetch(buffer_size=32)

# Directly Cites : https://keras.io/examples/vision/image_classification_from_scratch/
def NModel(input_shape,num_classes):
    inputs = keras.Input(shape = input_shape)
    x = data_augmentation(inputs)
    x = layers.Rescaling(1.0 / 255)(x)
    x = layers.Conv2D(32,3, strides = 2, padding= "same")(x)
    x = layers.BatchNormalization()(x)
    x = layers.Activation("relu")(x)

    x = layers.Conv2D(64,3,padding="Same")(x)
    x = layers.BatchNormalization()(x)
    x = layers.Activation("relu")(x)

    previous_block_activation = x

   
    for size in [128,256,512,728]:
       x = layers.Activation("relu")(x)
       x = layers.SeparableConv2D(size,3,padding = "same")(x)
       x = layers.BatchNormalization()(x)


       x = layers.Activation("relu")(x)
       x = layers.SeparableConv2D(size,3,padding = "same")(x)
       x = layers.BatchNormalization()(x)

       x = layers.MaxPooling2D(3,strides = 2, padding ="same")(x)  # Key for noisy images, use more than once?

       #Residual? TODO : Look up for comprehension
       residual = layers.Conv2D(size, 1, strides=2, padding="same")(
       previous_block_activation
       )
       x = layers.add([x, residual])  
       previous_block_activation = x

    # TODO : Look up for comprehension
    x = layers.SeparableConv2D(1024, 3, padding="same")(x)
    x = layers.BatchNormalization()(x)
    x = layers.Activation("relu")(x)

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
model = NModel(input_shape=image_size + (3,), num_classes=2)
keras.utils.plot_model(model, show_shapes=True)   
   
epochs = 100
callbacks = [keras.callbacks.ModelCheckpoint("save_at_{epoch}.h5"),
]

model.compile(
    optimizer = keras.optimizers.Adam(1e-3),
    loss = "binary_crossentropy",
    metrics = ["accuracy"],
)

model.fit(DataSet,epochs = epochs, callbacks = callbacks, validation_data = Validation)

img = keras.preprocessing.image.load_img(
    "Training_Data/sample-18255214-320-69.png", target_size=image_size
)

img_array = keras.preprocessing.image.img_to_array(img)
img_array = tf.expand_dims(img_array, 0)  # Create batch axis

predictions = model.predict(img_array)
score = predictions[0]

print(
    "This image is %.2f your coffee."
    % (100 * (score))
)



def main() :
    print("Nothing broke before here, this is exciting")


if __name__ == '__main__':
    main()





