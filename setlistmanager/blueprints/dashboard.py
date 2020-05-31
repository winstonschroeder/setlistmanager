from flask import (
    Blueprint, render_template
)

from setlistmanager.models import Setlist

bp = Blueprint('dashboard', __name__)


@bp.route('/dashboard')
def index():
    setlists = Setlist.query.all()
    return render_template('dashboard/index.html', setlists=setlists)
