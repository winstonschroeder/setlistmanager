from flask import Blueprint, json
from data_access import get_db, sqlresult_to_json, execute_query_cursor

bp = Blueprint("data", __name__)


@bp.route("/data/artists")
def artists_json():
    query = "SELECT artists as details FROM vjson_artists;"
    res = sqlresult_to_json(execute_query_cursor(query))
    return res


@bp.route("/data/songs")
def songs_json():
    query = "SELECT details FROM vjson_songs;"
    res = sqlresult_to_json(execute_query_cursor(query))
    return res


@bp.route("/data/shows")
def shows_json():
    query = "SELECT details FROM vjson_shows;"
    res = sqlresult_to_json(execute_query_cursor(query))
    return res


@bp.route("/data/setlists")
def setlists_json():
    query = "SELECT details FROM vjson_sets_per_setlist;"
    res = sqlresult_to_json(execute_query_cursor(query))
    return res
