# First Party Imports
import os
from concurrent.futures import ProcessPoolExecutor
import time
import re

# Third-party Imports
from flask import Blueprint, abort, jsonify, render_template, current_app
from flask import Flask, render_template, flash, request, redirect, url_for, make_response
from werkzeug.utils import secure_filename
from rq.job import Job


# Local Imports
from re_search.params import PARAMS
from meca.main import api
from re_search.tasks import api_task

import redis
from rq import Queue

executor = ProcessPoolExecutor(max_workers=5)
main = Blueprint('routes/main', __name__)

r = redis.Redis()
q = Queue(connection=r)

# *********************
# ROUTE FUNCTIONS
# *********************
@main.route("/about", methods=['GET', 'POST'])
def about():
    return render_template("about.html")

@main.route("/", methods=['GET'])
def landing():
    pending_jobs = request.args.get('pending_jobs')

    lib_key = request.cookies.get("lib-key")
    lib_id = request.cookies.get("lib-id")
    lib_key_cookie = lib_key is not None
    lib_id_cookie = lib_id is not None
    
    return render_template("main.html", lib_key=lib_key_cookie, lib_id=lib_id_cookie, pending_jobs=pending_jobs)

@main.route('/', methods=['POST'])
def landing_input():

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
        file.save(path)
        files.append(path)

    # API Call Section
    if files:
        job = q.enqueue(api_task, files)
        return redirect(url_for('routes/main.progress', job_id=job.get_id()))
        # return redirect(url_for('routes/main.landing', pending_jobs=len(files), job_id=job.get_id()))

    return redirect(url_for('routes/main.landing'))

@main.route('/progress/<job_id>')
def progress(job_id):
    return render_template('progress.html', job_id=job_id)

@main.route('/job-status/<job_id>', methods=['GET'])
def job_status(job_id):
    job = Job.fetch(job_id, connection=r)
    if job.is_finished:
        # Assuming job.result contains the URL to the PDF
        return jsonify({'status': 'finished', 'result': job.result})
    elif job.is_queued:
        return jsonify({'status': 'queued'})
    elif job.is_started:
        progress = job.meta.get('progress', 0)
        return jsonify({'status': 'started', 'progress': progress})
    elif job.is_failed:
        return jsonify({'status': 'failed'})
    else:
        return jsonify({'status': 'unknown'})
    
from flask import send_file

DOWNLOAD_DIRECTORY = os.path.abspath('pdfs')
@main.route('/download/<filename>', methods=['GET'])
def download(filename):
    safe_filename = re.sub(r'[^a-zA-Z0-9_\-.]', '', filename)
    file_path = os.path.join(DOWNLOAD_DIRECTORY, filename)
    
    # Check if the file exists
    loc = file_path.startswith(DOWNLOAD_DIRECTORY)
    if not os.path.isfile(file_path) and not loc:
        abort(404)  # File not found
    
    try:
        # Send the file for download
        return send_file(file_path, as_attachment=True)
    except Exception as e:
        # Handle unexpected errors
        return str(e), 500

@main.route('/cancel-job/<job_id>', methods=['POST'])
def cancel_job(job_id):
    job = Job.fetch(job_id, connection=r)
    job.cancel()
    return jsonify({'status': 'canceled'})

# *********************
# HELPER FUNCTIONS
# *********************
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in PARAMS['ALLOWED_EXTENSIONS']

def get_storage_path(filename: str):
    tmp = os.path.join(os.getcwd() ,PARAMS['UPLOAD_FOLDER'])
    if not os.path.exists(tmp): os.makedirs(tmp)
    return os.path.join(PARAMS['UPLOAD_FOLDER'], filename)

def meca_api(files, lib_key, lib_id):
    print('API Call Started')
    try:
        ret = api(files, lib_key, lib_id)
        print('API Call Successful')
    except Exception as e:
        print("API Call Failed, Error: ", e)


def test_api(self):
    print('API Call Started')
    time.sleep(5)  # Simulate time delay for API call
    print('API Call Ended')
    return 0