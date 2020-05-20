from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort

from setlistmanager.auth import login_required
from setlistmanager.db import get_db

bp = Blueprint('setlist', __name__)

@bp.route('/')
def index():
    db = get_db()
    setlists = db.execute(
        'SELECT s.id, s.name'
        ' FROM setlist s'
        ' ORDER BY name'
    ).fetchall()
    return render_template('setlist/index.html', setlists=setlists)



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

@bp.route('/create', methods=('GET', 'POST'))
def create():
    if request.method == 'POST':
        name = request.form['name']
        error = None

        if not name:
            error = 'name is required.'

        if error is not None:
            flash(error)
        else:
            db = get_db()
            db.execute(
                'INSERT INTO setlist (name)'
                ' VALUES (?)',
                (name,)
            )
            db.commit()
            return redirect(url_for('setlist.index'))

    return render_template('setlist/create.html')


@bp.route('/<int:id>/update', methods=('GET', 'POST'))
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
                'UPDATE setlist SET name = ?'
                ' WHERE id = ?',
                (name, id,)
            )
            db.commit()
            return redirect(url_for('setlist.index'))

    return render_template('setlist/update.html', setlist=setlist)


@bp.route('/<int:id>/delete', methods=('POST',))
def delete(id):
    get_setlist(id)
    db = get_db()
    db.execute('DELETE FROM setlist WHERE id = ?', (id,))
    db.commit()
    return redirect(url_for('setlist.index'))