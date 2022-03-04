import json
from flask import Flask, flash, render_template, request, redirect, session, url_for
from werkzeug.utils import secure_filename
import os
from datetime import datetime
from functions.readings.bin_read import binary_read
from functions.readings.custom_read import custom_read
from functions.readings.file_read import file_read
from functions.com.listDevice import get_device_list
import DAO.ConfigClassi

UPLOAD_FOLDER = './data/'
ALLOWED_EXTENSIONS = ['bst', 'mst', 'npy']
OUTPUT_FOLDER = './static/img/results/'

app = Flask(__name__)
app.config['SECRET_KEY'] = 'ww55z6e98a+f32h547r8e7'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['OUTPUT_FOLDER'] = OUTPUT_FOLDER
app.config['ALLOWED_EXTENSIONS'] = ALLOWED_EXTENSIONS

config=Config(logFilePath="logs/" +  datetime.now().strftime("%d:%m:%Y__%H:%M:%S"))


deviceTypes = {
    "scan_size": 0,
    "img_pixel": 0,
    "line_rate": 0,
    "offset": {
        "x": 0,
        "y": 0
    },
    "set_point": 0,
    "sample_bias": 0,
    "PID": {
        "KP": 0,
        "KI": 0,
        "KD": 0
    }
}


imageTitles = {
    "Image processing": ["Interpolation", "Colorization", "Method"],
    "Format": ["File format", "Zoom"]}

deviceTitles = {
    "Video processing": ["Interpolation", "Colorization", "Method"],
    "Format": ["Screenshot"]}


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']


@ app.route("/")
def main_menu():
    return render_template("mainMenu.html",)


@ app.route("/image")
def image_menu():
    return render_template("imageMenu.html",)


@ app.route("/image/upload", methods=['GET', 'POST'])
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


@ app.route("/image/watch/<file>", methods=['GET', 'POST'])
def watch_file(file):
    if os.path.exists(str(app.config['UPLOAD_FOLDER']) + str(file)) == False:
        return redirect(request.url)

    if (file.endswith((".npy"))):
        path, size, mode, format, palette = binary_read(
            file, app.config['UPLOAD_FOLDER'], app.config['OUTPUT_FOLDER'])
    elif (file.endswith(('.mst'))):
        path, size, mode, format, palette = file_read(
            file, app.config['UPLOAD_FOLDER'], app.config['OUTPUT_FOLDER'])
    elif (file.endswith(('.bst'))):
        path, size, mode, format, palette = custom_read(
            file, app.config['UPLOAD_FOLDER'], app.config['OUTPUT_FOLDER'])
    return render_template("/functionnalities/watchImage.html",
                           path=path,
                           size=size,
                           mode=mode,
                           format=format,
                           palette=palette,
                           titles=imageTitles,
                           toolkit="imagetoolkit")


@ app.route("/device")
def device_menu():
    return render_template("/deviceMenu.html")


@ app.route("/device/connect")
def connect_link():
    devDic = get_device_list(config)
    return redirect(url_for('watch_device'), devDic)


@ app.route("/device/watch", methods=['GET', 'POST'])
def watch_device():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'import' not in request.files:
            flash('No file part')
            print('No file part')
            return redirect(request.url)
        file = request.files['import']
        # If the user does not select a file, the browser submits an
        # empty file without a filename.
        if file.filename == '':
            flash('No selected file')
            print('No selected file')
            return redirect(request.url)
        if file and (file.filename.endswith('.json') or file.filename.endswith('.JSON')):
            imported = json.load(file)
            session["import"] = json.dumps(imported)
            return render_template("/functionnalities/watchDevice.html", titles=deviceTitles, toolkit="devicetoolkit", types=deviceTypes, imported=imported)
        else:
            flash('Wrong extension. Allowed extensions : .json, .JSON')
            print('Wrong extension. Allowed extensions : .json, .JSON')
            return redirect(request.url)

    if not session.get("import") is None:
        imported = json.loads(session.get("import"))
        return render_template("/functionnalities/watchDevice.html", titles=deviceTitles, toolkit="devicetoolkit", types=deviceTypes, imported=imported)
    return render_template("/functionnalities/watchDevice.html", titles=deviceTitles, toolkit="devicetoolkit", types=deviceTypes)


if __name__ == "__main__":
    port = 5000
    url = "http://127.0.0.1:{0}".format(port)
    app.run(use_reloader=False, debug=True, port=port)
