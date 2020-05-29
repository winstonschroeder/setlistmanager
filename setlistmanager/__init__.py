import os

from flask import Flask

from setlistmanager.db import db_session


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'setlistmanager.sqlite'),
    )

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    @app.teardown_appcontext
    def shutdown_session(exception=None):
        db_session.remove()

    from . import db
    db.init_app(app)

    from . import auth
    app.register_blueprint(auth.bp)

    from setlistmanager.blueprints import organizer
    app.register_blueprint(organizer.bp)
    app.add_url_rule('/', endpoint='index')

    from setlistmanager.blueprints import show
    app.register_blueprint(show.bp)
    app.add_url_rule('/shows', endpoint='index')

    from setlistmanager.blueprints import dashboard
    app.register_blueprint(dashboard.bp)

    return app
