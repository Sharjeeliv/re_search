# Third-party Imports
from flask import Blueprint, render_template, current_app

import os
# import gitmodules

from flask import Flask, render_template, flash, request, redirect, url_for, logging, make_response
from werkzeug.utils import secure_filename

from re_search.params import PARAMS

# Local Imports

main = Blueprint('routes/main', __name__)

@main.route("/", methods=['GET', 'POST'])
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
        main.logger.info(f'{LIB_KEY}')
        res = make_response(redirect(url_for('landing')))
        res.set_cookie("lib-key", LIB_KEY)
        return res

    LIB_ID = request.form.get("lib-id")
    if LIB_ID:
        main.logger.info(f'{LIB_ID}')
        res = make_response(redirect(url_for('landing')))
        res.set_cookie("lib-id", LIB_ID)
        return res

    # Check and Set Files
    input_files = request.files.getlist('file[]')
    if not input_files: return redirect(url_for('landing'))
    files = []

    for file in input_files:
        if not allowed_file(file.filename): continue
        filename = secure_filename(file.filename)

        path = os.path.join(PARAMS['UPLOAD_FOLDER'], filename)
        print(path)
        file.save(path)
        files.append(path)

    # if files: api(files, LIB_KEY, LIB_ID)

    return redirect(url_for('landing'))

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in PARAMS['ALLOWED_EXTENSIONS']