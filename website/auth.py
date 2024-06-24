from flask import Blueprint, render_template, request, flash, redirect, url_for
import time
from .models import User
from .models import Music
from .models import Playlist
from .models import InWhichPlaylist
from werkzeug.security import generate_password_hash, check_password_hash
from . import db
from flask_login import login_user, login_required, logout_user, current_user
import yt_dlp
import json
auth = Blueprint('auth', __name__)
urls = [1,1,[
    'https://youtu.be/ovTiSA9T-RU?si=H5r_oO7-tboMBeYB',
    'https://youtu.be/kkUWlcjmOew?si=LYhySQt4XrsUFOxP',
    'https://www.youtube.com/watch?v=ve6SQ3V8BSw'
]]
def get_URL_from_index(index):
    return urls[int(index)]


@auth.route("/login", methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        data = request.form
        email = data.get('email')
        password = data.get('password')

        user = User.query.filter_by(email=email).first()
        if user:
            if check_password_hash(user.password, password):
                flash("Logged in successfully", category="success")
                login_user(user,remember=True)

                return redirect(url_for('view.home'))
            else:
                flash("Incorrect password", category='error')
        else:
            flash("Email not exsist", category='error')
    return render_template("login.html",user = current_user)


@auth.route("/logout")
@login_required
def logout():
    logout_user()
    return render_template("logout.html",user = current_user)


@auth.route("/sigh-up", methods=['GET', 'POST'])
def register():
    if request.method == "POST":
        data = request.form
        email = data.get("email")
        firstName = data.get("firstName")
        password1 = data.get("password1")
        password2 = data.get("password2")
        if len(email) < 4:
            flash("Email address must be more than 4 characters", category="error")
        elif len(firstName) < 2:
            flash("First name must be more than 1 characters", category="error")
        elif len(password1) < 7:
            flash(
                "Password is too short.\nPassword must be more than 7 characters", category="error")
        elif password1 != password2:
            flash("Passwords don't match", category="error")
        else:

            if User.query.filter_by(email=email).first():
                flash("User is already exsisted", category="error")
                return render_template("sigh-up.html")

            new_user = User(email=email, password=generate_password_hash(
                password1, method="pbkdf2:sha256"), first_name=firstName, membership="Normal", limit = 5)
            login_user(new_user)
            db.session.add(new_user)
            db.session.commit()

            flash("Account created successfully", category="success")
            return redirect(url_for('view.home'))

    return render_template("sigh-up.html",user = current_user)


@auth.route('/search_url', methods=['POST'])
def search_url():
    youtube_url = request.form['search_query']
    ydl_opts = {
        'extract_flat': True,
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'webm',
            'preferredquality': '192',
        }],
    }
    music = Music.query.filter_by(original_url = youtube_url).first()
    is_update = False
    if music != None:
        url = music.audio_url
        l = url.find("expire")
        r = url.find("&",l)
        expire_time = int(url[l+7:r])
        current_time = time.time()
        if current_time > expire_time:
            is_update = True
    if music == None or is_update:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info_dict = ydl.extract_info(youtube_url, download=False)
            audio_url = info_dict['url']
            title = info_dict['title']
            id = info_dict['id']
            thumbnail_url =  max(info_dict['thumbnails'], key=lambda x: x['preference'])['url']
            artist = info_dict['uploader']
            new_music = Music(id = str(id),M_title = str(title), audio_url = str(audio_url), thumbnail_url = str(thumbnail_url), artist=str(artist), original_url = youtube_url)
            tar =  Music.query.filter_by(id=id).first()
            if tar == None:
                db.session.add(new_music)
                db.session.commit()
            else:
                tar.audio_url = audio_url
                tar.original_url = youtube_url
                db.session.commit()
    music = Music.query.filter_by(original_url = youtube_url).first()
    ret = dict()
    ret['status'] = 'sucess'
    ret['audio_url'] = music.audio_url
    ret['id'] = music.id
    ret['thumbnail_url'] = music.thumbnail_url
    ret['artist'] = music.artist
    ret['title'] = music.M_title
    return ret

@auth.route('/search_id', methods=['POST'])
def search_id():
    id = json.loads(request.form.get('search_query'))['id']
    music = Music.query.filter_by(id=id).first()
    if music == None :
        return {'status' : 'error'}
    url = music.audio_url
    l = url.find("expire")
    r = url.find("&",l)
    expire_time = int(url[l+7:r])
    current_time = time.time()
    is_update = True
    if current_time > expire_time:
        is_update = True
    if is_update:
        ydl_opts = {
        'extract_flat': True,
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'webm',
            'preferredquality': '192',
        }],
        }
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            youtube_url = 'https://www.youtube.com/watch?v='+id
            info_dict = ydl.extract_info(youtube_url, download=False)
            audio_url = info_dict['url']
            id = info_dict['id']
            tar =  Music.query.filter_by(id=id).first()
            tar.audio_url = audio_url
            db.session.commit()
    ret = dict()
    ret['status'] = 'success'
    ret['audio_url'] = music.audio_url
    ret['title'] = music.M_title
    return ret


@auth.route('/play/<path:index>',methods=['GET'])
def play(index):
    playlist = InWhichPlaylist.query.filter_by(P_id = index).all()

    playlist_data = []
    for music in playlist:
        data = Music.query.filter_by(id = music.M_id).first()
        id = data.id
        title = data.M_title
        artist = data.artist
        audio_url = data.audio_url
        thumbnail_url = data.thumbnail_url
        playlist_data.append({'title': title, 'artist': artist, 'audio_url': audio_url, 'thumbnail_url': thumbnail_url, 'id': id})

    return render_template('play.html', playlist_data=playlist_data, user = current_user, playlist_id = index)

@auth.route("/creat_playlist", methods=['POST'])
def creat_playlist():
	if request.method == 'POST':
		ret = dict()
		if current_user.is_anonymous:
			ret['status'] = 'error'
			return ret

		playlist_name = request.form.get('name')
		playlist_type = request.form.get('type')
		if playlist_name:
			ret['status'] = 'success'
			new_playlist = Playlist(P_title=playlist_name, P_type=playlist_type, UID=current_user.id)
			db.session.add(new_playlist)
			db.session.commit()
			ret['id'] = new_playlist.P_id
			return ret
		else:
			ret['status'] = 'success'
			return ret

@auth.route("/add_music_to_playlist", methods=['POST'])
def add_music_to_playlist():
	if request.method == 'POST':
		ret = dict()
		if current_user.is_anonymous:
			ret['status'] = 'error'
			ret['reason'] = 'not login'
			return ret

		which_playlist_id = request.form.get('playlist_id')
		which_music_id = request.form.get('music_id')
		if which_music_id and which_playlist_id:
			is_song_exist = Music.query.filter_by(id = which_music_id).first()
			is_already_exist = InWhichPlaylist.query.filter_by(M_id=which_music_id, P_id=which_playlist_id, UID=current_user.id).first()
			if not is_song_exist or  is_already_exist != None:
				ret['status'] = 'error'
				ret['reason'] = 'music id not exist or music already in playlist'
				return ret
			number_of_songs = len(InWhichPlaylist.query.filter_by(P_id = which_playlist_id).all())
			print(number_of_songs)
			if number_of_songs > current_user.limit :
				ret['status'] = 'error'
				ret['reason'] = 'reach the limit of songs'
				return ret;
			new_music_added_to_playlist = InWhichPlaylist(M_id=which_music_id, P_id=which_playlist_id, UID=current_user.id)
			db.session.add(new_music_added_to_playlist)
			db.session.commit()
			ret['status'] = 'success'
			return ret
		else:
			ret['status'] = 'error'
			ret['reason'] = 'music id or playlist id can\'t be empty'
			#flash("music id or playlist id can't be empty", category="error")
			return ret

@auth.route("/remove_music_from_playlist", methods=['POST'])
def remove_music_from_playlist():
	if request.method == "POST":
		ret = dict()
		if current_user.is_anonymous():
			ret['status'] = 'error'
			return ret
		Which_music_to_remove = request.form.get('music_id')
		Which_playlist = request.form.get('playlist_id')
		if Which_playlist and Which_music_to_remove:
			ret['status'] = 'success'
			tar = InWhichPlaylist.query.filter_by(P_id=Which_playlist, M_id=Which_music_to_remove, UID=current_user.id).first()
			if not tar:
				ret['status'] = 'error'
				return ret
			db.session.delete(tar)
			db.session.commit()
			return ret
		else:
			ret['status'] = 'error'
			return ret
@auth.route("/test", methods = ['GET'])
def test():
	return render_template("test.html",user = current_user)

@auth.route("/get_all_list", methods = ['POST'])
def get_all_list():
	if current_user.is_anonymous:
		return {"status" : "error"}
	playlists = Playlist.query.filter_by(UID=current_user.id).all()
	ret = {'datas' : []}
	for data in playlists:
		ret['datas'].append({'id' : data.P_id, 'title' : data.P_title})
	return ret
