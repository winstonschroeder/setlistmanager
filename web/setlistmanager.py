from itertools import groupby
from operator import itemgetter

from flask import Blueprint, json
from flask import render_template
from data_access import get_db

bp = Blueprint("setlistmanager", __name__)


@bp.route("/")
def index():
    return render_template("songs.html")

@bp.route("/setlists")
def setliststs():
    return render_template("setlists.html")


@bp.route("/shows")
def shows():
    return render_template("shows.html")

@bp.route("/live")
def live():
    return render_template("live.html")

@bp.route("/settings")
def settings():
    return render_template("settings.html")

@bp.route("/midi")
def midi():
    return render_template("midi.html")
