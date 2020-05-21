from flask import (
    Blueprint, flash, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort

from setlistmanager.db import get_db, db_session
from setlistmanager.models import Setlist

bp = Blueprint('setlist', __name__)


@bp.route('/setlists')
def index():
    db = get_db()
    setlists = Setlist.query.all()
    return render_template('setlist/index.html', setlists=setlists)


def get_setlist(id):
    setlist = Setlist.query.filter(Setlist.id == id).first()
    if setlist is None:
        abort(404, "setlist id {0} doesn't exist.".format(id))
    return setlist


@bp.route('/setlists/create', methods=('GET', 'POST'))
def create():
    if request.method == 'POST':
        name = request.form['name']
        error = None

        if not name:
            error = 'name is required.'

        if error is not None:
            flash(error)
        else:
            s = Setlist()
            s.name = name
            db_session.add(s)
            db_session.commit()
            return redirect(url_for('setlist.index'))

    return render_template('setlist/create.html')


@bp.route('/setlists/<int:id>/update', methods=('GET', 'POST'))
def update(id):
    setlist = get_setlist(id)

    if request.method == 'POST':
        name = request.form['name']
        error = None

        if not name:
            error = 'Name is required.'

        if error is not None:
            flash(error)
        else:
            db = get_db()
            db.execute(
                'UPDATE setlists SET name = ?'
                ' WHERE id = ?',
                (name, id,)
            )
            db.commit()
            return redirect(url_for('setlist.index'))

    return render_template('setlist/update.html', setlist=setlist)


@bp.route('/setlists/<int:id>/delete', methods=('POST',))
def delete(id):
    get_setlist(id)
    db = get_db()
    db.execute('DELETE FROM setlists WHERE id = ?', (id,))
    db.commit()
    return redirect(url_for('setlist.index'))
