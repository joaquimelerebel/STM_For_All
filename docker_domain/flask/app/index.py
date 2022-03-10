import json
import time
from functions.readings.save_image_linear import save_image
from functions.readings.file_reading_switch import switch_file
from functions.save import to_JSON as convertJSON
from flask import Flask, Response, flash, render_template, request, redirect, session, url_for, send_file
from werkzeug.utils import secure_filename
import os

UPLOAD_FOLDER = './data/'
ALLOWED_EXTENSIONS = ['bst', 'mst', 'npy']
OUTPUT_FOLDER = './static/img/results/'

app = Flask(__name__)
app.config['SECRET_KEY'] = os.urandom(12)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['OUTPUT_FOLDER'] = OUTPUT_FOLDER
app.config['ALLOWED_EXTENSIONS'] = ALLOWED_EXTENSIONS

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
    # To watch an image
    if os.path.exists(str(app.config['UPLOAD_FOLDER']) + str(file)) == False:
        return redirect(request.url)

    data = switch_file(file, app.config['UPLOAD_FOLDER'])
    path, size, mode, format, palette = save_image(
        file, data, app.config['OUTPUT_FOLDER'])
    path = url_for('static', filename='img/results/'+path)
    return render_template("/functionnalities/watchImage.html", file=file,
                           path=path,
                           size=size,
                           mode=mode,
                           format=format,
                           palette=palette,
                           titles=imageTitles,
                           toolkit="imagetoolkit")


@ app.route("/image/download/<file>", methods=['GET', 'POST'])
def download_file(file):
    # To save an image
    fileformat = 0
    if request.method == "POST" and request.form.get("formatdd"):
        fileformat = int(request.form.get("formatdd"))
        data = switch_file(file, app.config['UPLOAD_FOLDER'])

        response = save_image(
            file, data, app.config['OUTPUT_FOLDER'], format=fileformat)
        path = url_for('static', filename='img/results/'+response[0])[1:]
        if fileformat == 1:
            # For PNG format
            return send_file(path, as_attachment=True, download_name=time.strftime('%Y%m%d_%H%M%S') + "_image.png", mimetype='image/png')
        elif fileformat == 2:
            # For TIFF format
            return send_file(path, as_attachment=True, download_name=time.strftime('%Y%m%d_%H%M%S') + "_image.tiff", mimetype='image/tiff')
        else:
            # for JPEG format
            return send_file(path, as_attachment=True, download_name=time.strftime('%Y%m%d_%H%M%S') + "_image.jpg", mimetype='image/jpeg')
    flash("Downloading was unsuccessful", "error")
    return redirect(url_for('watch_file'))

# Device route


@ app.route("/device")
def device_menu():
    return render_template("/deviceMenu.html")


@ app.route("/device/connect")
def connect_link():
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
