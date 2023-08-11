# -*- coding: utf-8 -*-
"""multiclass_classificaton_of_fashion_mnist_dataset.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1YhOHrmfg5soE0bBG2wxvvEfotZ2DbkZM

## In this problem of multiclass classification , we are going to build a neural network to classify images of different items of clothing.
"""

import tensorflow as tf
from tensorflow.keras.datasets import fashion_mnist

#The data has already been sorted into training and test sets for us.
(train_data, train_labels), (test_data, test_labels) = fashion_mnist.load_data()

#Showing the first training example
print(f"Training Sample:\n{train_data[0]}\n")
print(f"Training Label:\n{train_labels[0]}\n")

"""Checking the shapes of the test and train data"""

train_data.shape, train_labels.shape

test_data.shape, test_labels.shape

#Plotting a single sample
import matplotlib.pyplot as plt
plt.imshow(train_data[0]);

#checking its label
train_labels[0]

#creating human readable labels of given training data

class_names = ["T-shirt/top", "Trousers", "Pullover", "Dress", "Coat", "Sandal", "Shirt", "Sneaker", "Bag", "Ankle boot"]

len(class_names)

#Plotting an example image and its label
index = 18
plt.imshow(train_data[index], cmap=plt.cm.binary)
plt.title(class_names[train_labels[index]])

import random
plt.figure(figsize=(7,7))
for i in range(4):
  ax = plt.subplot(2, 2, i+1)
  random_index = random.choice(range(len(train_data)))
  plt.imshow(train_data[random_index], cmap=plt.cm.binary)
  plt.title(class_names[train_labels[random_index]])
  plt.axis(False)

"""### Now lets build the multiclassification model"""

#setting the random seed
tf.random.set_seed(42)

#create the model
model_1 = tf.keras.Sequential([
    tf.keras.layers.Flatten(input_shape=(28,28)),
    tf.keras.layers.Dense(4, activation="relu"),
    tf.keras.layers.Dense(4, activation="relu"),
    tf.keras.layers.Dense(10, activation="softmax")
])


#compiling the model
model_1.compile(loss=tf.keras.losses.SparseCategoricalCrossentropy(),
                optimizer=tf.keras.optimizers.Adam(),
                metrics = ['accuracy'])

#Fitting the model
history = model_1.fit(train_data,
                      train_labels,
                      epochs=10,
                      validation_data=(test_data,test_labels))

#checkinng the model summary

model_1.summary()

"""## Now lets try to improve the accuracy by standardising or normalizing the data ( between 0 and 1)"""

#checking the min and max values of the training data
train_data.min(),train_data.max()

#normalizing the training and testing data
norm_train_data = train_data/255.0
norm_test_data = test_data/255.0

#checking our normalized data
norm_train_data.max(), norm_test_data.min()

#Using this normalised data on the same model we built above

#setting random seed
tf.random.set_seed(42)

#building the model
model_2 = tf.keras.Sequential([
    tf.keras.layers.Flatten(input_shape = (28,28)),
    tf.keras.layers.Dense(4, activation = "relu"),
    tf.keras.layers.Dense(4, activation = "relu"),
    tf.keras.layers.Dense(10, activation = "softmax")
])

#compiling the model
model_2.compile(loss=tf.keras.losses.SparseCategoricalCrossentropy(),
                optimizer=tf.keras.optimizers.Adam(),
                metrics = ['accuracy'])

#fitting the model
norm_history = model_2.fit(norm_train_data,
                           train_labels,
                           epochs=10,
                           validation_data = (norm_test_data, test_labels))

"""### Plotting the loss curves for normalized data and non-normalized data"""

import pandas as pd

#Plotting the non-normalized data loss curve
pd.DataFrame(history.history).plot(title = "Non_Normalized")

#Plotting the normalized data loss curve
pd.DataFrame(history.history).plot(title = "Normalized")

"""### Finding the ideal learning rate using the callback"""

#Using this normalised data on the same model we built above but with callback method

#setting random seed
tf.random.set_seed(42)

#building the model
model_3 = tf.keras.Sequential([
    tf.keras.layers.Flatten(input_shape = (28,28)),
    tf.keras.layers.Dense(4, activation = "relu"),
    tf.keras.layers.Dense(4, activation = "relu"),
    tf.keras.layers.Dense(10, activation = "softmax")
])

#compiling the model
model_3.compile(loss=tf.keras.losses.SparseCategoricalCrossentropy(),
                optimizer=tf.keras.optimizers.Adam(),
                metrics = ['accuracy'])

#creaating the learning rate callback
lr_schedular = tf.keras.callbacks.LearningRateScheduler(lambda epoch : 1e-3 * 10**(epoch/20))

#fitting the model
lr_norm_history = model_3.fit(norm_train_data,
                           train_labels,
                           epochs=40,
                           validation_data = (norm_test_data, test_labels),
                           callbacks=[lr_schedular])

#plotting the learning rate decay curve
import numpy as np
import matplotlib.pyplot as plt

lrs = 1e-3 * (10**(tf.range(40)/20))
plt.semilogx(lrs, lr_norm_history.history["loss"])
plt.xlabel("Learning Rate")
plt.ylabel("Loss")
plt.title("Finding the ideal learning rate")

"""## Lets now rebuild our model with the ideal learning rate"""

#Using this normalised data on the same model we built above but with callback method and ideal learning rate

#setting random seed
tf.random.set_seed(42)

#building the model
model_4 = tf.keras.Sequential([
    tf.keras.layers.Flatten(input_shape = (28,28)),
    tf.keras.layers.Dense(4, activation = "relu"),
    tf.keras.layers.Dense(4, activation = "relu"),
    tf.keras.layers.Dense(10, activation = "softmax")
])

#compiling the model
model_4.compile(loss=tf.keras.losses.SparseCategoricalCrossentropy(),
                optimizer=tf.keras.optimizers.Adam(lr=0.001),
                metrics = ['accuracy'])

#fitting the model
lr_norm_history = model_4.fit(norm_train_data,
                           train_labels,
                           epochs=40,
                           validation_data = (norm_test_data, test_labels))

"""### Evaulating our multiclass classification model"""

# Note: The following confusion matrix code is a remix of Scikit-Learn's
# plot_confusion_matrix function - https://scikit-learn.org/stable/modules/generated/sklearn.metrics.plot_confusion_matrix.html
# and Made with ML's introductory notebook - https://github.com/GokuMohandas/MadeWithML/blob/main/notebooks/08_Neural_Networks.ipynb
import itertools
from sklearn.metrics import confusion_matrix

# Our function needs a different name to sklearn's plot_confusion_matrix
def make_confusion_matrix(y_true, y_pred, classes=None, figsize=(10, 10), text_size=15):
  """Makes a labelled confusion matrix comparing predictions and ground truth labels.

  If classes is passed, confusion matrix will be labelled, if not, integer class values
  will be used.

  Args:
    y_true: Array of truth labels (must be same shape as y_pred).
    y_pred: Array of predicted labels (must be same shape as y_true).
    classes: Array of class labels (e.g. string form). If `None`, integer labels are used.
    figsize: Size of output figure (default=(10, 10)).
    text_size: Size of output figure text (default=15).

  Returns:
    A labelled confusion matrix plot comparing y_true and y_pred.

  Example usage:
    make_confusion_matrix(y_true=test_labels, # ground truth test labels
                          y_pred=y_preds, # predicted labels
                          classes=class_names, # array of class label names
                          figsize=(15, 15),
                          text_size=10)
  """
  # Create the confustion matrix
  cm = confusion_matrix(y_true, y_pred)
  cm_norm = cm.astype("float") / cm.sum(axis=1)[:, np.newaxis] # normalize it
  n_classes = cm.shape[0] # find the number of classes we're dealing with

  # Plot the figure and make it pretty
  fig, ax = plt.subplots(figsize=figsize)
  cax = ax.matshow(cm, cmap=plt.cm.Blues) # colors will represent how 'correct' a class is, darker == better
  fig.colorbar(cax)

  # Are there a list of classes?
  if classes:
    labels = classes
  else:
    labels = np.arange(cm.shape[0])

  # Label the axes
  ax.set(title="Confusion Matrix",
         xlabel="Predicted label",
         ylabel="True label",
         xticks=np.arange(n_classes), # create enough axis slots for each class
         yticks=np.arange(n_classes),
         xticklabels=labels, # axes will labeled with class names (if they exist) or ints
         yticklabels=labels)

  # Make x-axis labels appear on bottom
  ax.xaxis.set_label_position("bottom")
  ax.xaxis.tick_bottom()

  # Set the threshold for different colors
  threshold = (cm.max() + cm.min()) / 2.

  # Plot the text on each cell
  for i, j in itertools.product(range(cm.shape[0]), range(cm.shape[1])):
    plt.text(j, i, f"{cm[i, j]} ({cm_norm[i, j]*100:.1f}%)",
             horizontalalignment="center",
             color="white" if cm[i, j] > threshold else "black",
             size=text_size)

class_names

test_labels

#Lets make predictions with our model
y_probs = model_4.predict(norm_test_data)

#Viewing the firsr 5 predictions
y_probs[:5]

#plotting the ist data object
plt.imshow(train_data[0]);

#Making its prediction
y_probs[0], tf.argmax(y_probs[0]), class_names[tf.argmax(y_probs[0])]

#Now lets convert all the prediction probabilities into integers
y_preds = y_probs.argmax(axis=1)

#Viewing the first 1 predictions
y_preds[0], class_names[tf.argmax(y_probs[0])]

test_labels

"""Confusion Matrix"""

from sklearn.metrics import confusion_matrix
confusion_matrix(y_true=test_labels,
                 y_pred=y_preds)

#Lets make a better confusion matrix
make_confusion_matrix(y_true=test_labels,
                      y_pred=y_preds,
                      classes=class_names,
                      figsize=(15,15),
                      text_size = 10)

"""## Let's create a function to plot a random image along with its prediction."""

import random

# Create a function for plotting a random image along with its prediction
def plot_random_image(model, images, true_labels, classes):
  """Picks a random image, plots it and labels it with a predicted and truth label.

  Args:
    model: a trained model (trained on data similar to what's in images).
    images: a set of random images (in tensor form).
    true_labels: array of ground truth labels for images.
    classes: array of class names for images.

  Returns:
    A plot of a random image from `images` with a predicted class label from `model`
    as well as the truth class label from `true_labels`.
  """
  # Setup random integer
  i = random.randint(0, len(images))

  # Create predictions and targets
  target_image = images[i]
  pred_probs = model.predict(target_image.reshape(1, 28, 28)) # have to reshape to get into right size for model
  pred_label = classes[pred_probs.argmax()]
  true_label = classes[true_labels[i]]

  # Plot the target image
  plt.imshow(target_image, cmap=plt.cm.binary)

  # Change the color of the titles depending on if the prediction is right or wrong
  if pred_label == true_label:
    color = "green"
  else:
    color = "red"

  # Add xlabel information (prediction/true label)
  plt.xlabel("Pred: {} {:2.0f}% (True: {})".format(pred_label,
                                                   100*tf.reduce_max(pred_probs),
                                                   true_label),
                                                   color=color) # set the color to green or red

# Check out a random image as well as its prediction
plot_random_image(model=model_4,
                  images=test_data,
                  true_labels=test_labels,
                  classes=class_names)

"""# Patterns our model is learning"""

# Find the layers of our most recent model
model_4.layers

# Extracting a particular layer
model_4.layers[1]

# Getting the patterns of a layer in our network
weights, biases = model_4.layers[1].get_weights()

# Shape = 1 weight matrix the size of our input data (28x28) per neuron (4)
weights, weights.shape

"""The weights matrix is the same shape as the input data, which in our case is 784 (28x28 pixels). And there's a copy of the weights matrix for each neuron the in the selected layer (our selected layer has 4 neurons).

Each value in the weights matrix corresponds to how a particular value in the input data
influences the network's decisions.

#Now let's check out the bias vector.
"""

# Shape = 1 bias per neuron (we use 4 neurons in the first layer)
biases, biases.shape

"""Every neuron has a bias vector. Each of these is paired with a weight matrix.

The bias values get initialized as zeroes by default (using the bias_initializer parameter).

The bias vector dictates how much the patterns within the corresponding weights matrix should influence the next layer.
"""

#Now lets calculate the number of paramters in our model
model_4.summary()

"""Starting from the input layer, each subsequent layer's input is the output of the previous layer as shown below"""

from tensorflow.keras.utils import plot_model

# See the inputs and outputs of each layer
plot_model(model_4, show_shapes=True)

from google.colab.patches import cv2_imshow
img = cv2.imread('/content/pexels-vie-studio-4439457.jpg', cv2.IMREAD_UNCHANGED)
resized_image = cv2.resize(img,(700,300))
cv2_imshow(resized_image)