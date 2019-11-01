# coding: utf-8
from sqlalchemy import Column, DateTime, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
from sqlalchemy.schema import FetchedValue
from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()


class CartoonTable(db.Model):
    __tablename__ = 'cartoon_table'

    id = db.Column(db.Integer, primary_key=True)
    cartoon = db.Column(db.String(255), nullable=False)
    title = db.Column(db.String(30), nullable=False)
    picture = db.Column(db.String(255))
    collection_id = db.Column(db.ForeignKey('collection_tabe.id'), index=True)
    create_time = db.Column(db.DateTime, nullable=False)
    update_time = db.Column(db.DateTime)

    collection = db.relationship('CollectionTabe', primaryjoin='CartoonTable.collection_id == CollectionTabe.id', backref='cartoon_tables')


class CollectionTabe(db.Model):
    __tablename__ = 'collection_tabe'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(30), nullable=False)
    picture = db.Column(db.String(255))
    create_time = db.Column(db.DateTime, nullable=False)
    update_time = db.Column(db.DateTime)


class DrawTable(db.Model):
    __tablename__ = 'draw_table'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.ForeignKey('user_table.id'), nullable=False, index=True)
    image = db.Column(db.String(255), nullable=False)
    create_time = db.Column(db.DateTime, nullable=False)
    update_time = db.Column(db.DateTime)

    user = db.relationship('UserTable', primaryjoin='DrawTable.user_id == UserTable.id', backref='draw_tables')


class ManagerTable(db.Model):
    __tablename__ = 'manager_table'

    id = db.Column(db.Integer, primary_key=True)
    manager_name = db.Column(db.String(30), nullable=False, unique=True)
    password = db.Column(db.String(20), nullable=False)
    level = db.Column(db.Integer, nullable=False, server_default=db.FetchedValue())
    create_time = db.Column(db.DateTime, nullable=False)
    update_time = db.Column(db.DateTime)


class RecordingTable(db.Model):
    __tablename__ = 'recording_table'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.ForeignKey('user_table.id'), nullable=False, index=True)
    story_id = db.Column(db.ForeignKey('story_table.id'), nullable=False, index=True)
    recording = db.Column(db.String(255), nullable=False)
    title = db.Column(db.String(30), nullable=False)
    create_time = db.Column(db.DateTime, nullable=False)
    update_time = db.Column(db.DateTime)

    story = db.relationship('StoryTable', primaryjoin='RecordingTable.story_id == StoryTable.id', backref='recording_tables')
    user = db.relationship('UserTable', primaryjoin='RecordingTable.user_id == UserTable.id', backref='recording_tables')


class SongTable(db.Model):
    __tablename__ = 'song_table'

    id = db.Column(db.Integer, primary_key=True)
    song = db.Column(db.String(255), nullable=False)
    title = db.Column(db.String(30), nullable=False)
    picture = db.Column(db.String(255))
    singer = db.Column(db.String(30), nullable=False)
    create_time = db.Column(db.DateTime, nullable=False)
    update_time = db.Column(db.DateTime)


class StoryTable(db.Model):
    __tablename__ = 'story_table'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(30), nullable=False)
    text = db.Column(db.String(255), nullable=False)
    picture = db.Column(db.String(255))
    author = db.Column(db.String(30), nullable=False)
    create_time = db.Column(db.DateTime, nullable=False)
    update_time = db.Column(db.DateTime)


class UserTable(db.Model):
    __tablename__ = 'user_table'

    id = db.Column(db.Integer, primary_key=True)
    user_name = db.Column(db.String(30), nullable=False, unique=True)
    password = db.Column(db.String(16), nullable=False)
    tel = db.Column(db.Integer)
    mail = db.Column(db.String(50))
    create_time = db.Column(db.DateTime, nullable=False)
    update_time = db.Column(db.DateTime)
