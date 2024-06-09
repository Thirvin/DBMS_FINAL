from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func


'''class Music(db.Model):
    id = db.Column(db.String(1000), primary_key=True)
    title = db.Column(db.String(10000))
    play_url = db.Column(db.String(10000))
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150))
    first_name = db.Column(db.String(150))'''
class Music(db.Model):
    __tablename__ = 'Music'
    id = db.Column(db.string(1000), primary_key=True, autoincrement=True)
    M_type = db.Column(db.String(50))
    M_title = db.Column(db.String(10000), nullable=False)
    audio_url = db.Column(db.String(10000))
    thumbnail_url = db.Column(db.String(10000))
    SW_id = db.Column(db.Integer, db.ForeignKey('SongWriter.SW_id'))


class User(db.Model, UserMixin):
    __tablename__ = 'User'
    UID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    email = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(150), nullable=False)
    first_name = db.Column(db.String(150), nullable=False)
    last_name = db.Column(db.String(150))
    membership = db.Column(db.String(50))


class Playlist(db.Model):
    __tablename__ = 'Playlist'
    P_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    P_type = db.Column(db.String(50))
    P_title = db.Column(db.String(100), nullable=False)
    P_size = db.Column(db.Integer)
    is_private = db.Column(db.Boolean, default=True)
    UID = db.Column(db.Integer, db.ForeignKey('User.UID'))


class SongWriter(db.Model):
    __tablename__ = 'SongWriter'
    SW_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    SW_name = db.Column(db.String(100), nullable=False)


class InWhichPlaylist(db.Model):
    __tablename__ = 'InWhichPlaylist'
    M_id = db.Column(db.Integer, db.ForeignKey('Music.id'), primary_key=True)
    P_id = db.Column(db.Integer, db.ForeignKey('Playlist.P_id'), primary_key=True)
    UID = db.Column(db.Integer, db.ForeignKey('User.UID'), primary_key=True)
