# Examples

## Example | **One**
```
Please Enter 1 for compile 2 for test and 3 for both
2
You have selected test
Images of hot coffee

This image is 50.00 percent hot coffee and this image is 50.00 percent iced coffee.
This image is 50.00 percent hot coffee and this image is 50.00 percent iced coffee.
Images of iced coffee
This image is 50.00 percent hot coffee and this image is 50.00 percent iced coffee.
This image is 36.11 percent hot coffee and this image is 63.89 percent iced coffee.
```
**25% Accuracy**

## Example | **Two**

```
(venv) chris@dhcp-10-5-26-115 CSC_Independent % Python3 ignoresthermal.py
Found 464 files belonging to 2 classes.
Using 372 files for training.
2022-03-01 22:51:19.155735: I tensorflow/core/platform/cpu_feature_guard.cc:151] This TensorFlow binary is optimized with oneAPI Deep Neural Network Library (oneDNN) to use the following CPU instructions in performance-critical operations:  AVX2 FMA
To enable them in other operations, rebuild TensorFlow with the appropriate compiler flags.
Found 464 files belonging to 2 classes.
Using 92 files for validation.
Please Enter 1 for compile 2 for test and 3 for both or exit
2
You have selected test
Images of hot coffee
This image is 69.55 percent hot coffee and this image is 30.45 percent iced coffee.
This image is hot coffee

This image is 76.69 percent hot coffee and this image is 23.31 percent iced coffee.
This image is hot coffee

Images of iced coffee
This image is 40.32 percent hot coffee and this image is 59.68 percent iced coffee.
This image is cold coffee

This image is 23.73 percent hot coffee and this image is 76.27 percent iced coffee.
This image is cold coffee
```
**100% Accuracy**


## Example | **Three**

```
(venv) chris@dhcp-10-5-26-115 CSC_Independent % Python3 ignoresthermal.py
Found 464 files belonging to 2 classes.
Using 372 files for training.
2022-03-01 22:54:31.462946: I tensorflow/core/platform/cpu_feature_guard.cc:151] This TensorFlow binary is optimized with oneAPI Deep Neural Network Library (oneDNN) to use the following CPU instructions in performance-critical operations:  AVX2 FMA
To enable them in other operations, rebuild TensorFlow with the appropriate compiler flags.
Found 464 files belonging to 2 classes.
Using 92 files for validation.
Please Enter 1 for compile 2 for test and 3 for both or exit
2
You have selected test
Images of hot coffee
This image is 45.87 percent hot coffee and this image is 54.13 percent iced coffee.
This image is cold coffee

This image is 59.27 percent hot coffee and this image is 40.73 percent iced coffee.
This image is hot coffee

Images of iced coffee
This image is 62.37 percent hot coffee and this image is 37.63 percent iced coffee.
This image is hot coffee

This image is 64.00 percent hot coffee and this image is 36.00 percent iced coffee.
This image is hot coffee
```
**25% Accuracy**

```
96/96 [==============================] - 5s 47ms/step - loss: 0.6589 - accuracy: 0.6062 - val_loss: 0.6495 - val_accuracy: 0.6471
Epoch 496/500
96/96 [==============================] - 5s 46ms/step - loss: 0.6544 - accuracy: 0.6167 - val_loss: 0.6495 - val_accuracy: 0.6471
Epoch 497/500
96/96 [==============================] - 5s 46ms/step - loss: 0.6571 - accuracy: 0.6104 - val_loss: 0.6495 - val_accuracy: 0.6471
Epoch 498/500
96/96 [==============================] - 5s 45ms/step - loss: 0.6573 - accuracy: 0.6125 - val_loss: 0.6495 - val_accuracy: 0.6471
Epoch 499/500
96/96 [==============================] - 5s 45ms/step - loss: 0.6467 - accuracy: 0.6375 - val_loss: 0.6495 - val_accuracy: 0.6471
Epoch 500/500
96/96 [==============================] - 5s 45ms/step - loss: 0.6581 - accuracy: 0.6125 - val_loss: 0.6495 - val_accuracy: 0.6471
Current accuracy is 0.483008: 
You have selected test
Images of hot coffee
This image is 70.17 percent hot coffee and this image is 29.83 percent iced coffee.
This image is hot coffee

This image is 75.74 percent hot coffee and this image is 24.26 percent iced coffee.
This image is hot coffee

Images of iced coffee
This image is 49.10 percent hot coffee and this image is 50.90 percent iced coffee.
This image is cold coffee

This image is 15.17 percent hot coffee and this image is 84.83 percent iced coffee.
This image is cold coffee

Current final accuracy is 0.499959: 
```
```
2022-03-03 00:23:43.533698: I tensorflow/core/platform/cpu_feature_guard.cc:151] This TensorFlow binary is optimized with oneAPI Deep Neural Network Library (oneDNN) to use the following CPU instructions in performance-critical operations:  AVX2 FMA
To enable them in other operations, rebuild TensorFlow with the appropriate compiler flags.
Found 599 files belonging to 2 classes.
Using 119 files for validation.
Please Enter 1 for compile 2 for test and 3 for both or and key to close
2
Current accuracy is 0.492024: 
You have selected test
Images of hot coffee
This image is 77.73 percent hot coffee and this image is 22.27 percent iced coffee.
This image is hot coffee

This image is 67.81 percent hot coffee and this image is 32.19 percent iced coffee.
This image is hot coffee

Images of iced coffee
This image is 39.26 percent hot coffee and this image is 60.74 percent iced coffee.
This image is cold coffee

This image is 48.65 percent hot coffee and this image is 51.35 percent iced coffee.
This image is cold coffee

Current final accuracy is 0.508023 
```

**100% Accuracy!***

