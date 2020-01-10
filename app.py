from flask import Flask, render_template, request
import keras.backend.tensorflow_backend as tb
from check_image import check_image
from werkzeug.utils import secure_filename
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
    return render_template("index.html", info=info, image='')


@app.route('/check', methods=['POST'])
def check():
    tb._SYMBOLIC_SCOPE.value = True
    file = request.files['fileToUpload']
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        MYDIR = os.path.dirname(__file__)
        file.save(os.path.join(MYDIR + "/" + app.config['UPLOAD_FOLDER'], filename))
        file.save(os.path.join(MYDIR + "/static/images", filename))
        info = check_image(f'pictures/{filename}')
        return render_template("index.html", info=info, image=filename)

    return render_template("index.html", info="Error while processing file.")


if __name__ == '__main__':
    app.run(debug=True, port=5000, threaded=False)
