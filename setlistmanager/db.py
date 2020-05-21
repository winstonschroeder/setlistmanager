from datetime import datetime

import click
from flask import g
from flask.cli import with_appcontext
from sqlalchemy import create_engine, MetaData, Column, Integer, String, Table, ForeignKey, TIMESTAMP
from sqlalchemy.ext.declarative import declarative_base, declared_attr
from sqlalchemy.orm import scoped_session, sessionmaker, mapper

engine = create_engine('sqlite:////home/ruben/PycharmProjects/setlistmanager/instance/setlistmanager.sqlite',
                       convert_unicode=True)
metadata = MetaData()
db_session = scoped_session(sessionmaker(autocommit=False,
                                         autoflush=False,
                                         bind=engine))

user = Table('user', metadata,
             Column('id', Integer, primary_key=True),
             Column('name', String(50), unique=True),
             Column('password', String(50), unique=True)
             )


class User(object):
    query = db_session.query_property()

    def __init__(self, name=None, password=None):
        self.name = name
        self.password = password

    def __repr__(self):
        return '<User %r>' % (self.name)

metadata.create_all(bind=engine, tables=[user], checkfirst=True)
mapper(User, user)

class DeclarativeBaseModel(object):
    @declared_attr
    def __tablename__(cls):
        return cls.__name__.lower()

    __mapper_args__ = {'always_refresh': True}

    id = Column(Integer, primary_key=True)
    name = Column(String(50))


    @declared_attr
    def created_by(self):
        return Column(Integer, ForeignKey('user.id'))

    created_on = Column(TIMESTAMP, default=datetime.now())

    @declared_attr
    def modified_by(self):
        return Column(Integer, ForeignKey('user.id'))

    modified_on = Column(TIMESTAMP)

    def __init__(self, name: str = ''):
        self.name = name

    def __repr__(self):
        return '%s' % self.name


Base = declarative_base(cls=DeclarativeBaseModel)
Base.metadata = metadata
Base.query = db_session.query_property()


# noinspection PyUnresolvedReferences
def init_db():
    import setlistmanager.models
    Base.metadata.create_all(bind=engine)


def close_db(e=None):
    db = g.pop('db', None)
    if db is not None:
        db.close()


@click.command('init-db')
@with_appcontext
def init_db_command():
    """Clear the existing data and create new tables."""
    init_db()
    click.echo('Initialized the database.')


def init_app(app):
    app.teardown_appcontext(close_db)
    app.cli.add_command(init_db_command)
