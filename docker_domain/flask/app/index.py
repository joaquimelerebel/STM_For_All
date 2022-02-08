from distutils.log import error
import os
import re

from numpy import asarray, zeros, float64, array, load
from PIL import Image

from flask import Flask, flash, render_template, request, redirect, url_for
from werkzeug.utils import secure_filename

UPLOAD_FOLDER = './data'
ALLOWED_EXTENSIONS = ['mst', 'npy']
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

    return render_template("uploadFile.html")


@app.route("/watch/<file>", methods=['GET', 'POST'])
def watch_file(file):
    if os.path.exists("./data/" + file) == False:
        return redirect(request.url)

    if (file.endswith((".npy"))):
        path = binary_read(file)
        # render main and the image
        return render_template("image.html", imgpath=path)

    elif (file.endswith(('.mst'))):
        path = file_read(file)
        return render_template("image.html", imgpath=path)
    else:
        print("Wrong parameters")

# Takes in the name of a binary file, a deals with the data by creating an image of the array and returns bath


def binary_read(file):
    filedata = load("./data/" + file)
    height, width = filedata.shape

    # creating our array to have our image
    data = zeros((height, width, 3), dtype=float64)
    value = filedata*255/5
    data = array([value, value, value]).transpose()

    # importing image
    img = Image.fromarray(data, 'RGB')

    # if there is no output folder, create one
    if not os.path.exists(app.config['OUTPUT_FOLDER']):
        os.makedirs(app.config['OUTPUT_FOLDER'])

    # set the path and save the image in it
    path = app.config['OUTPUT_FOLDER'] + file[:-4] + '.jpg'
    img.save(path, 'JPEG')
    return path


# Takes in the name of a file, a deals with the data by creating an image of the array and returns bath
def file_read(file):
    # try opening output_filename, if there is none, let's do it in stdout
    if(isinstance(file, str)):
        f = open("./data/" + file, "r")

    # collecting the size of the array
    fileline = f.readline()
    size = re.sub(r"[\[-\]]", "", fileline).replace(" ", "").split(",")

    # preventing /n by retrieving 2 values from the width
    height, width = asarray(size, int)-[0, 1]

    # creating our array to have our image
    data = zeros((height, width, 3), dtype=float64)

    for h in range(0, height):
        line = f.readline()  # reading each line
        value = asarray(line.replace(" ", "").split(","), float64)[
            0:width]*(255/5)  # sanitizing the string and converting it (linear)
        data[h] = array([value, value, value]
                        ).transpose()  # making it RGB

    # image
    img = Image.fromarray(data, 'RGB')

    if not os.path.exists(app.config['OUTPUT_FOLDER']):
        os.makedirs(app.config['OUTPUT_FOLDER'])

    path = app.config['OUTPUT_FOLDER'] + file[:-4] + '.jpg'
    img.save(path, 'JPEG')

    # closing the file
    if(isinstance(file, str)):
        f.close()
    return path


if __name__ == "__main__":
    port = 5000
    url = "http://127.0.0.1:{0}".format(port)
    app.run(use_reloader=False, debug=True, port=port)
