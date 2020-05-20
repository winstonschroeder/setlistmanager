from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort

from setlistmanager.auth import login_required
from setlistmanager.db import get_db

bp = Blueprint('setlist_sandbox', __name__)

@bp.route('/setlist_sandbox')
def index():
    db = get_db()
    setlists = db.execute(
        'SELECT s.id, s.name'
        ' FROM setlist s'
        ' ORDER BY name'
    ).fetchall()
    return render_template('controls_sandbox/setlist_control.html', setlists=setlists)



def get_setlist(id):
    setlist = get_db().execute(
        'SELECT s.id, name'
        ' FROM setlist s'
        ' WHERE s.id = ?',
        (id,)
    ).fetchone()

    if setlist is None:
        abort(404, "setlist id {0} doesn't exist.".format(id))

    return setlist
