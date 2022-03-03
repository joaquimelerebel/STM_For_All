from flask import Flask, flash, render_template, request, redirect, url_for
from werkzeug.utils import secure_filename

import os

from functions.readings.bin_read import binary_read
from functions.readings.custom_read import custom_read
from functions.readings.file_read import file_read

UPLOAD_FOLDER = './data/'
ALLOWED_EXTENSIONS = ['bst', 'mst', 'npy']
OUTPUT_FOLDER = './static/img/results/'

app = Flask(__name__)
app.config['SECRET_KEY'] = 'ww55z6e98a+f32h547r8e7'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['OUTPUT_FOLDER'] = OUTPUT_FOLDER
app.config['ALLOWED_EXTENSIONS'] = ALLOWED_EXTENSIONS


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower(
           ) in app.config['ALLOWED_EXTENSIONS']


@app.route("/")
def main_menu():
    return render_template("mainMenu.html",)


@app.route("/image")
def image_menu():
    return render_template("imageMenu.html",)


@app.route("/image/upload", methods=['GET', 'POST'])
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
            if not os.path.exists(app.config['UPLOAD_FOLDER']):
                os.makedirs(app.config['UPLOAD_FOLDER'])
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            return redirect(url_for('watch_file', file=filename))
        else:
            flash('Wrong extension. Allowed extensions : ' +
                  str(ALLOWED_EXTENSIONS).strip('[]'))
            print('Wrong extension. Allowed extensions : ' +
                  str(ALLOWED_EXTENSIONS).strip('[]'))
            return redirect(request.url)

    return render_template("/functionnalities/uploadFile.html", format=app.config['ALLOWED_EXTENSIONS'])


@app.route("/image/watch/<file>", methods=['GET', 'POST'])
def watch_file(file):
    if os.path.exists(str(app.config['UPLOAD_FOLDER']) + str(file)) == False:
        return redirect(request.url)

    if (file.endswith((".npy"))):
        path, size, mode, format, palette = binary_read(
            file, app.config['UPLOAD_FOLDER'], app.config['OUTPUT_FOLDER'])
        # render main and the image
        return render_template("/functionnalities/watchImage.html", path=path, size=size, mode=mode, format=format, palette=palette)

    elif (file.endswith(('.mst'))):
        path, size, mode, format, palette = file_read(
            file, app.config['UPLOAD_FOLDER'], app.config['OUTPUT_FOLDER'])
        return render_template("/functionnalities/watchImage.html", path=path, size=size, mode=mode, format=format, palette=palette)
    elif (file.endswith(('.bst'))):
        path, size, mode, format, palette = custom_read(
            file, app.config['UPLOAD_FOLDER'], app.config['OUTPUT_FOLDER'])
        return render_template("/functionnalities/watchImage.html", path=path, size=size, mode=mode, format=format, palette=palette)
    else:
        print("Wrong parameters")


if __name__ == "__main__":
    port = 5000
    url = "http://127.0.0.1:{0}".format(port)
    app.run(use_reloader=False, debug=True, port=port)
