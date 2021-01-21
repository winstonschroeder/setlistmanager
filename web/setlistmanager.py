from flask import Blueprint, json
from flask import flash
from flask import g
from flask import redirect
from flask import render_template
from flask import request
from flask import jsonify, make_response

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
    # if request.is_json:
    #     req = request.get_json()
    #     print (req)
    #
    #     response_body = {
    #         "message": "JSON received!",
    #         "sender": req.get("name")
    #     }
    #
    #     res = make_response(jsonify(response_body), 200)

    setlists = get_setlists_of_band()
    return render_template("setlists.html", setlists=setlists)


@bp.route("/shows")
def shows():
    shows = get_shows_of_band()
    return render_template("shows.html", shows=shows)


@bp.route("/live")
def live():
    return render_template("live.html")


@bp.route("/settings")
def settings():
    return render_template("settings.html")


@bp.route("/midi")
def midi():
    return render_template("midi.html")


@bp.route("/setlists/json")
def setlists_json():
    #data = sqlresult_to_json(get_setlists_of_band())
    band_id = 1
    query = "SELECT sl.id, sl.band_id, sl.name as setlist_name, s.name as set_name " \
            "FROM setlists sl " \
            "LEFT JOIN sets2setlists s2sl " \
            "ON sl.id = s2sl.setlist_id " \
            "LEFT JOIN sets s " \
            "ON s2sl.set_id = s.id " #\
            # " WHERE sl.id = ?"
    #data = sqlresult_to_json(get_setlists_of_band())
    # data = sqlresult_to_json(execute_query(query, (band_id,)))
    data = sqlresult_to_json(execute_query(query))
    res = make_response(data, 200)
    return data


############################################# data requests ##################################

def sqlresult_to_json(sqlresult):
    items = [dict(zip([key[0] for key in sqlresult.description], row)) for row in sqlresult]
    return json.dumps(items)

def execute_query(query, **parameters):
    # TODO: fix parameter selection in execute_query.
    db = get_db()
    cursor = db.cursor()
    res = cursor.execute(query, parameters)
    return res

def get_songs_of_band(band_id=None):
    db = get_db()
    if band_id is None:
        return db.execute(
            "SELECT s.id, s.band_id, b.name as band_name, s.name as song_name, a.name as composer " \
            "FROM songs s " \
            "LEFT JOIN artists a " \
            "ON a.id = s.composer_id " \
            "LEFT JOIN bands b " \
            "ON b.id = s.band_id " \
            ).fetchall()
    else:
        return db.execute(
            "SELECT s.id, s.band_id, b.name as band_name, s.name as song_name, a.name as composer " \
            "FROM songs s " \
            "LEFT JOIN artists a " \
            "ON a.id = s.composer_id " \
            "LEFT JOIN bands b " \
            "ON b.id = s.band_id " \
            "WHERE b.id = ?",
            (band_id,),
        ).fetchall()


def get_setlists_of_band(band_id=None):
    """ new version returns cursor results instead of table results, providing column headers. """
    db = get_db()
    cursor = db.cursor()
    query = "SELECT sl.id, sl.band_id, sl.name as setlist_name, s.name as set_name " \
            "FROM setlists sl " \
            "LEFT JOIN sets2setlists s2sl " \
            "ON sl.id = s2sl.setlist_id " \
            "LEFT JOIN sets s " \
            "ON s2sl.set_id = s.id"
    if band_id is not None:
        query = query + " WHERE sl.band_id = ?"
        return cursor.execute(query, (band_id,), )
    return cursor.execute(query)

def get_setlists_of_band_old(band_id=None):
    db = get_db()
    query = "SELECT sl.id, sl.band_id, sl.name as setlist_name, s.name as set_name " \
            "FROM setlists sl " \
            "LEFT JOIN sets2setlists s2sl " \
            "ON sl.id = s2sl.setlist_id " \
            "LEFT JOIN sets s " \
            "ON s2sl.set_id = s.id"
    if band_id is not None:
        query = query + " WHERE sl.band_id = ?"
        return db.execute(query, (band_id,), ).fetchall()
    return db.execute(query).fetchall()


def get_shows_of_band(band_id=None):
    db = get_db()
    query = "SELECT s.id, b.id as band_id, s.name, s.date, b.name " \
            "FROM shows s " \
            "LEFT JOIN shows2bands s2b " \
            "ON s.id = s2b.show_id " \
            "LEFT JOIN bands b " \
            "ON s2b.band_id = b.id "
    if band_id is not None:
        query = query + " WHERE s2b.band_id = ?"
        return db.execute(query, (band_id,), ).fetchall()
    return db.execute(query).fetchall()
