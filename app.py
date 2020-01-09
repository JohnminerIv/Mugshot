from flask import Flask, render_template, request, redirect, url_for
import keras.backend.tensorflow_backend as tb
from check_image import check_image
from keras.preprocessing.image import img_to_array
from keras.models import load_model
import numpy as np
import argparse
import imutils
import cv2
app = Flask(__name__)


@app.route('/')
def index():
    tb._SYMBOLIC_SCOPE.value = True
    info = check_image()
    return render_template("index.html", info=info)


if __name__ == '__main__':
    app.run(debug=True, port=5000, threaded=False)
