import json
import time
import pathlib
import os
from types import SimpleNamespace
from datetime import datetime
from flask import Flask, Response, flash, render_template, request, redirect, session, url_for, send_file, jsonify
from werkzeug.utils import secure_filename

# custom imports
from functions.readings.save_image_linear import save_image
from functions.readings.file_reading_switch import switch_file
from functions.save import to_JSON as convertJSON
from functions.readings.bin_read import binary_read
from functions.readings.custom_read import custom_read
from functions.readings.file_read import file_read
from functions.com.listDevice import get_device_list
import functions.com.interaction as scan
import functions.com.cmd_int as cmd

import DAO.ConfigClass as ConfigClass


UPLOAD_FOLDER = './data/'
ALLOWED_EXTENSIONS = ['bst', 'mst', 'npy']
OUTPUT_FOLDER = './static/img/results/'

app = Flask(__name__)
app.config['SECRET_KEY'] = os.urandom(12)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['OUTPUT_FOLDER'] = OUTPUT_FOLDER
app.config['ALLOWED_EXTENSIONS'] = ALLOWED_EXTENSIONS

# check that the log folder exists
try:
    cpath = pathlib.Path(__file__).parent.resolve()
    if not os.path.exists(str(cpath) + "/logs/"):
        os.mkdir(str(cpath) + "/logs")
    logFilePath = str(cpath) + "/logs/" + \
        datetime.now().strftime("%d:%m:%Y__%H:%M:%S")
    # create the log file
    config = ConfigClass.Config(logFilePath=logFilePath)
    cmd.print_verbose_WHITE(
        config, f"[STATUS] logFile Created at {logFilePath}")
except:
    flash("Error during the config creation")
    raise()

# Config file JSON for the STM
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

# Title sections for the image toolkit
imageTitles = {
    "Image processing": ["Interpolation", "Colorization", "Method"],
    "Format": ["File format", "Zoom"]}

# Title sections for the device toolkit
deviceTitles = {
    "Video processing": ["Interpolation", "Colorization", "Method"],
    "Format": ["Screenshot"]}


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

# Main route


@ app.route("/")
def main_menu():
    return render_template("mainMenu.html",)

# Image route


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
    colors = []
    # To watch an image
    if os.path.exists(str(app.config['UPLOAD_FOLDER']) + str(file)) == False:
        return redirect(request.url)
    # Get the data corresponding to the format of the uploaded file
    data = switch_file(file, app.config['UPLOAD_FOLDER'])
    # If the user preselected colors
    if not session.get("colors") is None:
        colors = session.get("colors")
    # Get the path to the image (and some other info)
    filename, size, mode, format, palette = save_image(
        file, data, app.config['OUTPUT_FOLDER'], colors=colors)
    path = url_for('static', filename='img/results/'+filename)

    # Render the watchImage template
    return render_template("/functionnalities/watchImage.html", file=file,
                           path=path,
                           filename=filename,
                           size=size,
                           mode=mode,
                           format=format,
                           palette=palette,
                           titles=imageTitles,
                           colors=colors,
                           toolkit="imagetoolkit")


@ app.route("/image/download/<file>", methods=['GET', 'POST'])
def download_file(file):
    # To save an image
    fileformat = 0
    colors = []
    if request.method == "POST" and request.form.get("formatdd"):
        fileformat = int(request.form.get("formatdd"))
        data = switch_file(file, app.config['UPLOAD_FOLDER'])

        # If the user preselected colors
        if not session.get("colors") is None:
            colors = session.get("colors")
        response = save_image(
            file, data, app.config['OUTPUT_FOLDER'], format=fileformat, colors=colors)
        path = url_for('static', filename='img/results/'+response[0])[1:]
        if fileformat == 1:
            # for JPEG format
            return send_file(path, as_attachment=True, download_name=time.strftime('%Y%m%d_%H%M%S') + "_image.jpg", mimetype='image/jpeg')
        elif fileformat == 2:
            # For TIFF format
            return send_file(path, as_attachment=True, download_name=time.strftime('%Y%m%d_%H%M%S') + "_image.tiff", mimetype='image/tiff')
        else:
            # For PNG format
            return send_file(path, as_attachment=True, download_name=time.strftime('%Y%m%d_%H%M%S') + "_image.png", mimetype='image/png')
    flash("Downloading was unsuccessful", "error")
    return redirect(url_for('watch_file', file=file))


@ app.route("/image/color/<file>", methods=['GET', 'POST'])
def color_file(file):
    # To color an image
    if request.method == "POST":
        if 'apply' in request.form:
            if request.form.get("colorBlack") and request.form.get("colorMid") and request.form.get("colorWhite"):
                colorRange = [request.form.get("colorBlack"), request.form.get(
                    "colorMid"), request.form.get("colorWhite")]
                session["colors"] = colorRange
        else:
            if not session.get("colors") is None:
                session.pop("colors")
    return redirect(url_for('watch_file', file=file))
# Device route


@ app.route("/device")
def device_menu():
    if 'devices' in request.args:
        device = request.args.get('devices')
        selected = device
        cmd.print_verbose_WHITE(config, f"[REQ] ping {device}")

        try:
            status = scan.ping(config, selected)
        except Exception as ex:
            flash("not the right device", "error")
            status = False
            #if config.debug:
            #    raise ex
    else:
        selected = ""
        status = False

    if not "devices" in session:
        devices = get_device_list(config)
    else:
        devices = session.get("devices")
    return render_template("/deviceMenu.html", devices=devices, selected=selected, status=status)


@ app.route("/device/connect")
def connect_link():
    if not "devices" in session:
        session["dev"] = request.args.get('devices')
    return redirect(url_for('watch_device'))


@ app.route("/device/image/scan/launch", methods=['POST'])
def launch_scan():
    # check if session exist
    cmd.print_verbose_WHITE(config, f"[LOG] trying to launch scan")
    if not "dev" in session:
        cmd.eprint_RED(config,
                       f"[ERR] trying to start scan without device")
        flash("device not available on session", "error")
        result = {"isScanLaunched": False, "error": "No device on session"}
        return jsonify(result)

    if not "import" in session:
        cmd.eprint_RED(config, f"[ERR] no config available")
        flash("set your config before you start the scan", "error")
        result = {"isScanLaunched": False, "error": "No config available"}
        return jsonify(result)

    path = session.get("dev")

    # create the new scanner
    try:
        config.devicePath = path
        scanner = scan.Scanner(config, json.loads(
            session["import"], object_hook=lambda d: SimpleNamespace(**d)))
        config.newScanner(scanner)
        # launch the scan
        scanner.start_scan()
        flash("Scan successfully launched", "success")
        result = {"isScanLaunched": True, "error": ""}
        return jsonify(result)

    except Exception as x:
        flash("did not get to start the scan", "error")
        cmd.eprint_RED(config, f"[ERR] while starting the scan")
        result = {"isScanLaunched": False,
                  "error": "error while starting the scan"}
        if config.debug:
            raise
        return jsonify(result)


@ app.route("/device/image/color", methods=['GET', 'POST'])
def color_device():
    # To color an image
    if request.method == "POST":
        if 'apply' in request.form:
            if request.form.get("colorBlack") and request.form.get("colorMid") and request.form.get("colorWhite"):
                colorRange = [request.form.get("colorBlack"), request.form.get(
                    "colorMid"), request.form.get("colorWhite")]
                session["colors"] = colorRange
        else:
            if not session.get("colors") is None:
                session.pop("colors")
    return redirect(url_for('update_image_device'))

# same but in dynamic
@ app.route("/device/image/color2", methods=['GET', 'POST'])
def color_device2():
    # To color an image
    if request.method == "POST":
        cmd.print_verbose_WHITE( config, f"[LOG] color change")
        if 'apply' in request.form:
            if request.form.get("colorBlack") and request.form.get("colorMid") and request.form.get("colorWhite"):
                colorRange = [request.form.get("colorBlack"), request.form.get(
                    "colorMid"), request.form.get("colorWhite")]
                session["colors"] = colorRange
        else:
            if not session.get("colors") is None:
                session.pop("colors")

        if not type(config.scanner) == int : 
            cmd.print_verbose_WHITE( config, f"[LOG] image update")
            matrix = config.scanner.getMatrix()
            result = {"isReloadable": False, "Path": ""}
            response = save_image(
                    "scan_update_" + time.strftime('%Y%m%d_%H%M%S'), matrix, app.config['OUTPUT_FOLDER'], colors=colors)
            path = url_for(
                    'static', filename='img/results/'+response[0])[1:]
            isReloadable=True
        else :
            path = ""
            isReloadable=False
        result = {"isReloadable": isReloadable, "Path": path, "black" : colorRange[0], "mid": colorRange[1], "white":colorRange[2]}
    return jsonify(result)


@ app.route("/device/image/scan/update", methods=['POST', 'GET'])
def update_image_device():

    colors = []
    if not session.get("colors") is None:
        colors = session.get("colors")

    cmd.print_verbose_WHITE( config, f"[LOG] trying to update image")
    if not config.scanner == None:
        # checks on the current status of the scan
        if config.scanner.hasUpdated() or len(colors) > 0:
            cmd.print_verbose_WHITE( config, f"[LOG] matrix updatable")
            matrix = config.scanner.getMatrix()
            # If the user preselected colors
            response = save_image(
                "scan_update_" + time.strftime('%Y%m%d_%H%M%S'), matrix, app.config['OUTPUT_FOLDER'], colors=colors)
            path = url_for(
                'static', filename='img/results/'+response[0])[1:]
            # add image
            result = {"isReloadable": True, "Path": path}
        else:
            result = {"isReloadable": False, "Path": ""}

        # true or false (need to reload the image or not)
        return jsonify(result)
    return redirect(url_for("device_menu"))


@ app.route("/device/watch", methods=['GET', 'POST'])
def watch_device():
    # added by ulysse, needs to be modified
    if (not session.get("dev") is None) or (not request.args.get('device') is None):
        if not request.args.get('device') is None:
            path = request.args.get('device')
        if not session.get("dev") is None:
            path = session.get("dev")
    else:
        path = None

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
            return render_template("/functionnalities/watchDevice.html", path=path, titles=deviceTitles, toolkit="devicetoolkit", types=deviceTypes, imported=imported)
        else:
            flash('Wrong extension. Allowed extensions : .json, .JSON', 'error')
            return redirect(request.url)
    if not session.get("import") is None:
        imported = json.loads(session.get("import"))
        return render_template("/functionnalities/watchDevice.html", path=path, titles=deviceTitles, toolkit="devicetoolkit", types=deviceTypes, imported=imported)

    return render_template("/functionnalities/watchDevice.html", path=path, titles=deviceTitles, toolkit="devicetoolkit", types=deviceTypes)


@ app.route("/device/config/save", methods=['GET', 'POST'])
def save_config():
    if request.method == 'POST':
        req = request.form
        convert = convertJSON.to_JSON()
        convert.set_all(req.get('scan_size'), req.get('img_pixel'),
                        req.get('line_rate'), req.get('x'), req.get('y'),
                        req.get('set_point'), req.get('sample_bias'),
                        req.get('KP'), req.get('KI'), req.get('KD'))
        jsonfile = convert.json_output()
        if 'export' in request.form:
            return Response(jsonfile,
                            mimetype='application/json',
                            headers={'Content-Disposition': 'attachment; filename=' + time.strftime('%Y%m%d_%H%M%S') + '_config.json'})
        elif 'set' in request.form:
            session["import"] = jsonfile
            flash("The config was successfully set", "success")
            return redirect(url_for('watch_device'))
    flash("The file wasn't exported", "error")
    return redirect(url_for('watch_device'))


if __name__ == "__main__":
    port = 5000
    url = "http://127.0.0.1:{0}".format(port)
    app.run(use_reloader=False, debug=True, port=port)
