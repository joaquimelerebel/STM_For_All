import json
from functions.save import to_JSON
from flask import Flask, flash, render_template, request, redirect, session, url_for
from werkzeug.utils import secure_filename
import os
import pathlib
from datetime import datetime
# custom import
from functions.readings.bin_read import binary_read
from functions.readings.custom_read import custom_read
from functions.readings.file_read import file_read
from functions.com.listDevice import get_device_list
from functions.com.interaction import ping
import functions.com.cmd_int as cmd
import DAO.ConfigClass as ConfigClass


UPLOAD_FOLDER = './data/'
ALLOWED_EXTENSIONS = ['bst', 'mst', 'npy']
OUTPUT_FOLDER = './static/img/results/'

app = Flask(__name__)
app.config['SECRET_KEY'] = 'ww55z6e98a+f32h547r8e7'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['OUTPUT_FOLDER'] = OUTPUT_FOLDER
app.config['ALLOWED_EXTENSIONS'] = ALLOWED_EXTENSIONS

#check that the log folder exists
try :
    cpath=pathlib.Path(__file__).resolve()
    if not os.path.exists(str(cpath) + "logs/") :
        os.mkdir(str(cpath) + "logs")
    # create the log file 
    config=ConfigClass.Config(logFilePath= str(cpath) + "logs/" + datetime.now().strftime("%d:%m:%Y__%H:%M:%S"))
except : 
    print("Error during the config creation")
    raise()

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
            flash('No file part', 'error')
            return redirect(request.url)
        file = request.files['file']
        # If the user does not select a file, the browser submits an
        # empty file without a filename.
        if file.filename == '':
            flash('No selected file', 'error')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            if not os.path.exists(app.config['UPLOAD_FOLDER']):
                os.makedirs(app.config['UPLOAD_FOLDER'])
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            return redirect(url_for('watch_file', file=filename))
        else:
            flash('Wrong extension. Allowed extensions : ' +
                  str(ALLOWED_EXTENSIONS).strip('[]'), 'error')
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
    if not request.args.get('devices') is None :
        device = request.args.get('devices');
        selected = device;
        cmd.print_verbose_WHITE(config.logFilePath, f"[REQ] ping {device}");
        
        #DEBUG--TODO
        try :
            status = ping( config, selected );
        except Exception as ex :
            flash(ex)
            status=False
    else : 
        selected="";
        status=False;


    if session.get("devices") is None:
        devices = get_device_list(config)
    else :
        devices = session.get("devices") 
    return render_template("/deviceMenu.html", devices=devices, selected=selected, status=status)


@ app.route("/device/connect")
def connect_link():
    if request.args.get('devices') is None :
        return redirect(url_for('watch_device'))
    else :
        # pass information to the new page
        dev = request.args.get('devices');
        return redirect(url_for('watch_device'))



@ app.route("/device/watch", methods=['GET', 'POST'])
def watch_device():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'import' not in request.files:
            flash('No file part', 'error')
            return redirect(request.url)
        file = request.files['import']
        # If the user does not select a file, the browser submits an
        # empty file without a filename.
        if file.filename == '':
            flash('No selected file', 'error')
            return redirect(request.url)
        if file and (file.filename.endswith('.json') or file.filename.endswith('.JSON')):
            imported = json.load(file)
            session["import"] = json.dumps(imported)
            flash("File successfully imported", "success")
            return render_template("/functionnalities/watchDevice.html", titles=deviceTitles, toolkit="devicetoolkit", types=deviceTypes, imported=imported)
        else:
            flash('Wrong extension. Allowed extensions : .json, .JSON', 'error')
            return redirect(request.url)

    if not session.get("import") is None:
        imported = json.loads(session.get("import"))
        return render_template("/functionnalities/watchDevice.html", titles=deviceTitles, toolkit="devicetoolkit", types=deviceTypes, imported=imported)
    return render_template("/functionnalities/watchDevice.html", titles=deviceTitles, toolkit="devicetoolkit", types=deviceTypes)


@ app.route("/device/config/save", methods=['GET', 'POST'])
def save_config():
    if request.method == 'POST':
        flash(request.form, "success")
        if not session.get("import") is None:
            imported = json.loads(session.get("import"))
            return render_template("/functionnalities/watchDevice.html", titles=deviceTitles, toolkit="devicetoolkit", types=deviceTypes, imported=imported)
    return render_template("/functionnalities/watchDevice.html", titles=deviceTitles, toolkit="devicetoolkit", types=deviceTypes)


if __name__ == "__main__":
    port = 5000
    url = "http://127.0.0.1:{0}".format(port)
    app.run(use_reloader=False, debug=True, port=port)
