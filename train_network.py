import matplotlib
from keras.preprocessing.image import ImageDataGenerator
from keras.optimizers import Adam
from sklearn.model_selection import train_test_split
from keras.preprocessing.image import img_to_array
from keras.utils import to_categorical
from pyimagesearch.lenet import LeNet
from imutils import paths
import numpy as np
import argparse
import random
import cv2
import os


def randomize_imgs(image_paths):
    paths = sorted(list(image_paths))
    random.seed(42)
    return random.shuffle(paths)


def process_and_label(image_paths, desired_type):
    labels = []
    data = []
    for image_path in image_paths:
        # load the image, pre-process it, and store it in the data list
        image = cv2.imread(image_path)
        image = cv2.resize(image, (56, 56))
        image = img_to_array(image)
        data.append(image)

        # get the label from the image path and update the labels list
        label = image_path.split(os.path.sep)[-2]
        label = 1 if label == desired_type else 0
        labels.append(label)
    return labels, data


def scale_put_in_np_array(labels, data):
    data = np.array(data, dtype="float") / 255.0
    labels = np.array(labels)
    return labels, data


def create_model(labels, data, location_of_model, EPOCHS=50, INIT_LR=1e-3, BS=32):
    (trainX, testX, trainY, testY) = train_test_split(data, labels, test_size=0.25, random_state=42)

    # convert the labels from integers to vectors
    trainY = to_categorical(trainY, num_classes=2)
    testY = to_categorical(testY, num_classes=2)

    # construct the image generator for data augmentation
    aug = ImageDataGenerator(
        rotation_range=30, width_shift_range=0.1, height_shift_range=0.1,
        shear_range=0.2, zoom_range=0.2, horizontal_flip=True, fill_mode="nearest")

    # initialize the model
    model = LeNet.build(width=56, height=56, depth=3, classes=2)
    opt = Adam(lr=INIT_LR, decay=INIT_LR / EPOCHS)
    model.compile(loss="binary_crossentropy", optimizer=opt, metrics=["accuracy"])

    # train the network
    H = model.fit_generator(aug.flow(
        trainX, trainY, batch_size=BS),
        validation_data=(testX, testY),
        steps_per_epoch=len(trainX) // BS,
        epochs=EPOCHS, verbose=1)

    # save the model to disk
    model.save(location_of_model)


if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument("-d", "--dataset", required=True, help="path to input dataset")
    ap.add_argument("-m", "--model", required=True, help="path to output model")
    args = vars(ap.parse_args())
    matplotlib.use("Agg")
    # grab the image paths and randomly shuffle them
    image_paths = randomize_imgs(paths.list_images(args["dataset"]))
    # initialize the data and labels
    labels, data = process_and_label(image_paths, 'mug')
    labels, data = scale_put_in_np_array(labels, data)
    create_model(labels, data, args["model"])
