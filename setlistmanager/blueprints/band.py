from flask import (
    Blueprint, render_template
)

from setlistmanager.models import Band

bp = Blueprint('dashboard', __name__)


@bp.route('/band')
def index():
    bands = Band.query.all()
    return render_template('band/index.html', setlists=bands)