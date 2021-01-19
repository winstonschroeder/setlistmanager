from flask import Blueprint
from flask import flash
from flask import g
from flask import redirect
from flask import render_template
from flask import request
from flask import url_for
from werkzeug.exceptions import abort

from web.auth import login_required
from data_access import get_db

bp = Blueprint("setlistmanager", __name__)

@bp.route("/")
def index():
    """Show all the songs, most recent first."""
    db = get_db()
    bands = db.execute(
        "SELECT b.id, b.name FROM bands b ORDER BY b.name ASC"
    )
    songs = get_songs_of_band(None)
    return render_template("repertoire.html", songs=songs, bands=bands)

@bp.route("/<int:band_id>", methods=("GET", "POST",))
def repertoire_filtered(band_id):
    """Show all the songs, most recent first."""
    db = get_db()
    bands = db.execute(
        "SELECT b.id, b.name FROM bands b ORDER BY b.name ASC"
    )
    songs = get_songs_of_band(band_id)
    return render_template("repertoire.html", songs=songs, bands=bands)

@bp.route("/setlists")
def setliststs():
    db = get_db()
    setlists = get_setlists_of_band()
    return render_template("setlists.html", setlists = setlists)

def get_songs_of_band(band_id = None):
    db = get_db()
    if band_id is None:
        return db.execute(
            "SELECT s.id, s.band_id, b.name as band_name, s.name as song_name, a.name as composer "
            "FROM songs s "
            "LEFT JOIN artists a "
            "ON a.id = s.composer_id "
            "LEFT JOIN bands b "
            "ON b.id = s.band_id"
        ).fetchall()
    else:
        return db.execute(
            "SELECT s.id, s.band_id, b.name as band_name, s.name as song_name, a.name as composer "
            "FROM songs s "
            "LEFT JOIN artists a "
            "ON a.id = s.composer_id "
            "LEFT JOIN bands b "
            "ON b.id = s.band_id "
            "WHERE b.id = ?",
            (band_id,),
        ).fetchall()

def get_setlists_of_band(band_id = None):
    db = get_db()
    query = "SELECT sl.id, sl.band_id, sl.name, s.name " \
        "FROM setlists sl " \
        "LEFT JOIN sets2setlists s2sl " \
        "ON sl.id = s2sl.setlist_id " \
        "LEFT JOIN sets s " \
        "ON s2sl.set_id = s.id"
    if band_id is not None:
        query = query + " WHERE sl.band_id = ?"
        return db.execute(query, (band_id,),).fetchall()
    return db.execute(query).fetchall()