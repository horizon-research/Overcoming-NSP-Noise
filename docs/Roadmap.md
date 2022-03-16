# Christopher Bruinsma | Independent Study Roadmap | Spring ‘22


## Aims
The aims of this research are to *a)* investigate the effects of dark-current on an image sensor by inducing the kind of heat that would be expected of a sensor in a near-sensor processing configuration, *b)* train a neural network using image samples taken from the  thermal noise induced image sensor in various heat states, *c)* to compare the efficacy of training a neural network on near-noiseless images versus noisy images, and measuring how well a common object can be identified by an object detection neural network. The metric that would define how well the neural network has functioned is its task accuracy as was the case in both [1][2].

More on task *a)*, the sensor should be heated in intervals of 5°C ranging from room temperature as the control to around 80° C as this was the thermal range of the sensor *Kodukula et al.* in figure 3 [1]. In sum, the aims of this are to test to train an object detection neural network on images with thermal noise in order to circumvent the use of a denoising neural network entirely.

 This research aims to come up with a solution to the dark-current noise created by near-sensor processing and the final deliverable will be a paper reporting on the findings of this research and the hope is that we will have processed enough images to see a more effective neural network that can capably handle images with a high amount of dark current noise which would allow for a reduction in overhead for near sensor processing. 

This begs the question: what is the plan this semester?
> Project Plan Independent Study : https://docs.google.com/spreadsheets/u/0/d/1wlkRtAA392qumB3aZUPkizF1CW8MMfCJSjqskhHpLUU/edit
This is my tentative plan for the semester that takes into account the online portion of the semester.

## Materials 
- [x] A heat gun to be used for inducing dark current noise

- [x] An image sensor of some kind to be heated up (you mentioned something about a FLIR sensor, does this come with a lens?)

- [x] Imaging software to connect and capture images (to interface with 2)

- [x] A Neural Network (how should these be implemented? Tensorflow? PyTorch?)

- [ ] Around 1000 Images for object detection **[This is being neared at now 599 images]**

- [x] A set of coffee cups to image that are iced and hot varietals. 

- [x] Camera Specific Capture Code using Spinnaker SDK 





**Works Cited**
> [1] Dynamic Temperature Management of Near-Sensor Processing for Energy-Efficient High-Fidelity 
   Imaging. Kodukula Et Al.

> [2] Dirty Pixels: Towards End-to-End Image Processing and Perception Diamond Et. Al.





