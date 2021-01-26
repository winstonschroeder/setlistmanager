import os
from flask import Flask


def create_app(test_config=None):
    """Create and configure an instance of the Flask application."""
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY="dev",
        DATABASE=os.path.join(app.instance_path, "../../setlistmanager.db"),
    )

    if test_config is None:
        app.config.from_pyfile("config.py", silent=True)
    else:
        app.config.update(test_config)

    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    import data_access
    data_access.init_app(app)

    from web import auth, setlistmanager, data

    app.register_blueprint(auth.bp)
    app.register_blueprint(setlistmanager.bp)
    app.register_blueprint(data.bp)

    app.add_url_rule("/", endpoint="index")
    return app


if __name__ == '__main__':
    app = create_app()
    app.run(host="127.0.0.1", port=5000, debug=True)
