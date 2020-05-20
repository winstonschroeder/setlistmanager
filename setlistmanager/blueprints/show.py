import jsons
from flask import (
    Blueprint, render_template, jsonify
)

from models.show import Show

bp = Blueprint('show', __name__)


@bp.route('/shows/data')
def get_shows():
    res = jsonify(jsons.dump(Show.query.all(), strip_privates=True))
    return res


@bp.route('/shows')
def index():
    return render_template('show/index.html')
