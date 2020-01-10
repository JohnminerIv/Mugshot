from flask import Flask, render_template, request, redirect, url_for, flash
import keras.backend.tensorflow_backend as tb
from check_image import check_image
from werkzeug.utils import secure_filename
from keras.preprocessing.image import img_to_array
from keras.models import load_model
import numpy as np
import argparse
import imutils
import cv2
import os
UPLOAD_FOLDER = 'pictures'
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/')
def index():
    tb._SYMBOLIC_SCOPE.value = True
    info = check_image()
    print()
    return render_template("index.html", info=info)


@app.route('/check', methods=['POST'])
def check():
    tb._SYMBOLIC_SCOPE.value = True
    file = request.files['fileToUpload']
    # info = check_image(image)
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        MYDIR = os.path.dirname(__file__)
        file.save(os.path.join(MYDIR + "/" + app.config['UPLOAD_FOLDER'], filename))
        info = check_image(f'pictures/{filename}')
        return render_template("index.html", info=info)

    return '''
    <!doctype html>
    <title>Upload new File</title>
    <h1>Upload new File</h1>
    <form method=post enctype=multipart/form-data>
      <input type=file name=file>
      <input type=submit value=Upload>
    </form>
    '''


if __name__ == '__main__':
    app.run(debug=True, port=5000, threaded=False)
