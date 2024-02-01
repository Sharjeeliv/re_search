# First Party Imports
import os

# Third-party Imports
from flask import Blueprint, render_template, current_app
from flask import Flask, render_template, flash, request, redirect, url_for, make_response
from werkzeug.utils import secure_filename

# Local Imports
from re_search.params import PARAMS
from meca.main import api


main = Blueprint('routes/main', __name__)

@main.route("/about", methods=['GET', 'POST'])
def about():
    return render_template("about.html")

@main.route("/", methods=['GET'])
def landing():
    lib_key = request.cookies.get("lib-key")
    lib_id = request.cookies.get("lib-id")

    lib_key_cookie = lib_key is not None
    lib_id_cookie = lib_id is not None
    
    return render_template("main.html", lib_key=lib_key_cookie, lib_id=lib_id_cookie)

@main.route('/', methods=['POST'])
def landing_input():
    # Check and Set Lib Key Cookies
    LIB_KEY = request.form.get("lib-key")

    if LIB_KEY:
        current_app.logger.info(f'{LIB_KEY}')
        res = make_response(redirect(url_for('routes/main.landing')))
        res.set_cookie("lib-key", LIB_KEY)
        return res
    else: LIB_KEY = request.cookies.get("lib-key")

    LIB_ID = request.form.get("lib-id")
    if LIB_ID:
        current_app.logger.info(f'{LIB_ID}')
        res = make_response(redirect(url_for('routes/main.landing')))
        res.set_cookie("lib-id", LIB_ID)
        return res
    else: LIB_ID = request.cookies.get("lib-id")

    print(LIB_KEY, LIB_ID)
    # Check and Set Files
    input_files = request.files.getlist('file[]')
    if not input_files: return redirect(url_for('routes/main.landing'))
    files = []

    for file in input_files:
        if not allowed_file(file.filename): continue
        filename = secure_filename(file.filename)
        path = get_storage_path(filename)
        print(path)
        file.save(path)
        files.append(path)

    # Call MECA API
    if files:
        print('Beginning api call')
        flash(f'Uploading {len(files)} files to Zotero', 'warning')
        api(files, LIB_KEY, LIB_ID)

    return redirect(url_for('routes/main.landing'))

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in PARAMS['ALLOWED_EXTENSIONS']

def get_storage_path(filename: str):
    tmp = os.path.join(os.getcwd() ,PARAMS['UPLOAD_FOLDER'])
    if not os.path.exists(tmp): os.makedirs(tmp)
    return os.path.join(PARAMS['UPLOAD_FOLDER'], filename)