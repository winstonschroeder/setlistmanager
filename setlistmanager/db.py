import sqlite3

import click
from flask import current_app, g
from flask.cli import with_appcontext
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import scoped_session, sessionmaker

engine = create_engine('sqlite:////home/ruben/PycharmProjects/setlistmanager/instance/setlistmanager.sqlite', convert_unicode=True)
db_session = scoped_session(sessionmaker(autocommit=False,
                                         autoflush=False,
                                         bind=engine))
Base = declarative_base()
Base.query = db_session.query_property()


def get_db():
    if 'db' not in g:
        g.db = sqlite3.connect(
            current_app.config['DATABASE'],
            detect_types=sqlite3.PARSE_DECLTYPES
        )
        g.db.row_factory = sqlite3.Row

    return g.db


def init_db():
    # import all modules here that might define models so that
    # they will be registered properly on the metadata.  Otherwise
    # you will have to import them first before calling init_db()

    import models.band
    import models.instrument
    import models.preset
    import models.setlist
    import models.show
    import models.song
    import models.songsection
    import models.user
    import models.venue

    Base.metadata.create_all(bind=engine)


def close_db(e=None):
    db = g.pop('db', None)

    if db is not None:
        db.close()


# def init_db():
#     db = get_db()
#     # TODO: Import Models here and implement all mentioned in https://flask.palletsprojects.com/en/1.1.x/patterns/sqlalchemy/#declarative
#     with current_app.open_resource('schema.sql') as f:
#         db.executescript(f.read().decode('utf8'))


@click.command('init-db')
@with_appcontext
def init_db_command():
    """Clear the existing data and create new tables."""
    init_db()
    click.echo('Initialized the database.')


def init_app(app):
    app.teardown_appcontext(close_db)
    app.cli.add_command(init_db_command)
