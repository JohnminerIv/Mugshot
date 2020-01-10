from keras.preprocessing.image import img_to_array
from keras.models import load_model
import numpy as np
import cv2


def check_image(image=None):
    # load the image
    if image is None:
        return "No image processed."
    else:
        image = cv2.imread(image)
    # pre-process the image for classification
    image = cv2.resize(image, (56, 56))
    image = image.astype("float") / 255.0
    image = img_to_array(image)
    image = np.expand_dims(image, axis=0)
    # load the trained convolutional neural network
    print("[INFO] loading network...")
    model = load_model('mug_not_mug.model')
    # classify the input image
    (notmug, mug) = model.predict(image)[0]
    # build the label
    label = "Mug" if mug > notmug else "Not Mug"
    proba = mug if mug > notmug else notmug
    label = "{}: {:.2f}%".format(label, proba * 100)
    return label


if __name__ == '__main__':
    print("Bowl.jpg is")
    print(check_image('examples/Bowl.jpg'))
