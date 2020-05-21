import jsons
from flask import (
    Blueprint, render_template, jsonify
)

from setlistmanager.models import Band, Setlist, Song

bp = Blueprint('organizer', __name__)


@bp.route('/setlists')
def get_shows():
    res = jsonify(jsons.dump(Setlist.query.all(), strip_privates=True))
    return res

@bp.route('/songs')
def get_songs():
    res = jsonify(jsons.dump(Song.query.all(), strip_privates=True))
    return res


@bp.route('/')
def index():
    return render_template('organizer/index.html', bands=Band.query.all())
