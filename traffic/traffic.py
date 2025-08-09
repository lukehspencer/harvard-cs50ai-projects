import cv2
import numpy as np
import os
import sys
import tensorflow as tf

from sklearn.model_selection import train_test_split

EPOCHS = 10
IMG_WIDTH = 30
IMG_HEIGHT = 30
NUM_CATEGORIES = 43
TEST_SIZE = 0.4


def main():

    # Check command-line arguments
    if len(sys.argv) not in [2, 3]:
        sys.exit("Usage: python traffic.py data_directory [model.h5]")

    # Get image arrays and labels for all image files
    images, labels = load_data(sys.argv[1])

    # Split data into training and testing sets
    labels = tf.keras.utils.to_categorical(labels)
    x_train, x_test, y_train, y_test = train_test_split(
        np.array(images), np.array(labels), test_size=TEST_SIZE
    )

    # Get a compiled neural network
    model = get_model()

    # Fit model on training data
    model.fit(x_train, y_train, epochs=EPOCHS)

    # Evaluate neural network performance
    model.evaluate(x_test,  y_test, verbose=2)

    # Save model to file
    if len(sys.argv) == 3:
        filename = sys.argv[2]
        model.save(filename)
        print(f"Model saved to {filename}.")


def load_data(data_dir):
    """
    Load image data from directory `data_dir`.

    Assume `data_dir` has one directory named after each category, numbered
    0 through NUM_CATEGORIES - 1. Inside each category directory will be some
    number of image files.

    Return tuple `(images, labels)`. `images` should be a list of all
    of the images in the data directory, where each image is formatted as a
    numpy ndarray with dimensions IMG_WIDTH x IMG_HEIGHT x 3. `labels` should
    be a list of integer labels, representing the categories for each of the
    corresponding `images`.
    """
    images = []
    labels = []
    for category in range(NUM_CATEGORIES):
        # Gets directory that contains every image from a category
        category_folder = os.path.join(data_dir, str(category))
        
        for file in os.listdir(category_folder):
            # Gets the exact image from its category
            file_path = os.path.join(category_folder, file)
            
            # Reads image in as a numpy.ndarray
            img = cv2.imread(file_path)
            
            # Resizes image 
            resized_img = cv2.resize(img, (IMG_WIDTH, IMG_HEIGHT))
            
            # Normalizes image pixel values to be between 0 and 1
            resized_img = resized_img.astype(np.float32) / 255.0 
            
            # Append image and label to lists
            images.append(resized_img)
            labels.append(category)

    return (images, labels)

    raise NotImplementedError


def get_model():
    """
    Returns a compiled convolutional neural network model. Assume that the
    `input_shape` of the first layer is `(IMG_WIDTH, IMG_HEIGHT, 3)`.
    The output layer should have `NUM_CATEGORIES` units, one for each category.
    """
    model = tf.keras.models.Sequential([
        # First feature map (learns 32 filters using 3x3 kernel)
        tf.keras.layers.Conv2D(
            32, (3,3), activation="relu", input_shape = (IMG_WIDTH, IMG_HEIGHT, 3)
        ),
        
        # Pooling layer from first feature map
        tf.keras.layers.MaxPooling2D(pool_size=(2,2)),

        # Second feature map from previous pooling
        tf.keras.layers.Conv2D(
            64, (3,3), activation="relu", input_shape = (IMG_WIDTH, IMG_HEIGHT, 3)
        ),
        
        # Pooling layer from second feature map
        tf.keras.layers.MaxPooling2D(pool_size=(2,2)),

        # Flatten output for input layer
        tf.keras.layers.Flatten(),

        # Input layer with 128 neurons 
        tf.keras.layers.Dense(128, activation="relu"),
        
        # Drop 50% of the neurons to help prevent overfitting 
        tf.keras.layers.Dropout(0.5),

        # Output layer with 43 neurons for each category and activation function of softmax to give probabilities for each category
        tf.keras.layers.Dense(NUM_CATEGORIES, activation="softmax")
    ])

    # Compile model
    model.compile(
        optimizer="adam",
        loss="categorical_crossentropy",
        metrics=["accuracy"]
    )

    return model

    raise NotImplementedError


if __name__ == "__main__":
    main()
