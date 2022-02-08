import os
import re

from numpy import asarray, zeros, float64, array, load
from PIL import Image

from flask import Flask, flash, render_template, request, redirect, url_for
from werkzeug.utils import secure_filename

UPLOAD_FOLDER = './data'
ALLOWED_EXTENSIONS = ['', 'npy']

app = Flask(__name__)

app.config['SECRET_KEY'] = 'ww55z6e98a+f32h547r8e7'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['ALLOWED_EXTENSIONS'] = ALLOWED_EXTENSIONS


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower(
           ) in app.config['ALLOWED_EXTENSIONS']


@app.route("/", methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            print('No file part')
            return redirect(request.url)
        file = request.files['file']
        # If the user does not select a file, the browser submits an
        # empty file without a filename.
        if file.filename == '':
            flash('No selected file')
            print('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            print('Saved in ', os.path.join(app.config['UPLOAD_FOLDER']))
            return redirect(url_for('upload_file', name="/watch"))
        else:
            flash('Wrong extension. Allowed extensions : ' +
                  str(ALLOWED_EXTENSIONS).strip('[]'))
            print('Wrong extension. Allowed extensions : ' +
                  str(ALLOWED_EXTENSIONS).strip('[]'))
            return redirect(request.url)

    return render_template("main.html")


@app.route("/watch", methods=['GET', 'POST'])
def watch_file():
    return '<h1> welcome to watch </h1>'


if __name__ == "__main__":
    app.debug = True
    app.run()
