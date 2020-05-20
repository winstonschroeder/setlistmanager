from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort
from setlistmanager.auth import login_required
from setlistmanager.db import get_db

bp = Blueprint('dashboard', __name__)

@bp.route('/')
def index():
    return render_template('dashboard/index.html')