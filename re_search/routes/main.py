# Third-party Imports
from flask import Blueprint, render_template, current_app

# Local Imports

main = Blueprint('routes/main', __name__)

@main.route("/", methods=['GET', 'POST'])
def home():
    return render_template('home.html')