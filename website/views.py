from flask import Blueprint, render_template
from flask_login import login_required, current_user

views = Blueprint('view', __name__)


@views.route('/')
def home():
    return render_template("home.html",user = current_user)
