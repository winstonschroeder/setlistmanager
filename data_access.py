import sqlite3
import json
from sqlite3.dbapi2 import Connection

import click
from flask import current_app, g
from flask.cli import with_appcontext


def get_db():
    if 'db' not in g:
        g.db = sqlite3.connect(
            current_app.config['DATABASE'],
            detect_types=sqlite3.PARSE_DECLTYPES
        )
        g.db.row_factory = sqlite3.Row

    return g.db


def close_db(e=None):
    db = g.pop('db', None)

    if db is not None:
        db.close()

def init_db():
    db = get_db()
    with current_app.open_resource('schema.sql') as f:
        db.executescript(f.read().decode('utf8'))


@click.command('init-db')
@with_appcontext
def init_db_command():
    """Clear the existing data and create new tables."""
    init_db()
    click.echo('Initialized the database.')

def init_app(app):
    app.teardown_appcontext(close_db)
    app.cli.add_command(init_db_command)

con: Connection = None
dbname = './../setlistmanager.db'

def connect_db():
    return sqlite3.connect(dbname)

def get_all_songs_as_json():
    query = "SELECT * FROM v_songs_per_band;"
    return query_to_json(query)

def query_to_json(query):
    con = connect_db()
    curs = con.cursor()
    res = curs.execute(query)
    items = []
    for row in res:
        for key in curs.description:
            items.append({key[0]: value for value in row})
    return json.dumps(items)

if __name__ == '__main__':
    print(get_all_songs_as_json())