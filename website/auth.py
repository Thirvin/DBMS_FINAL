from flask import Blueprint, render_template, request, flash, redirect, url_for
from .models import User
from .models import Music
from werkzeug.security import generate_password_hash, check_password_hash
from . import db
from flask_login import login_user, login_required, logout_user, current_user
import yt_dlp
auth = Blueprint('auth', __name__)
urls = [[
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
                password1, method="sha256"), first_name=firstName)
            login_user(new_user)
            db.session.add(new_user)
            db.session.commit()

            flash("Account created successfully", category="success")
            return redirect(url_for('view.home'))

    return render_template("sigh-up.html",user = current_user)


@auth.route('/search_url', methods=['POST'])
def search_url():
    print(dict(request.form))
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
	
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info_dict = ydl.extract_info(youtube_url, download=False)
        audio_url = info_dict['url']
        title = info_dict['title']
        id = info_dict['id']
        new_music = Music(id = str(id),M_title = str(title), audio_url = str(audio_url))
        if Music.query.filter_by(id=id).first() == None:
            db.session.add(new_music)
            db.session.commit()	
    music = Music.query.filter_by(id=id).first()
    ret = dict()
    ret['status'] = 'sucess'
    ret['url'] = music.audio_url
    ret['id'] = music.id
    ret['title'] = music.M_title
    return ret

@auth.route('/search_id', methods=['POST'])
def search_id():
    id = request.form['search_query']
    music = Music.query.filter_by(id=id).first()
    if music == None :
        return {'status' : 'error'}
    ret = dict()
    ret['status'] = 'success'
    ret['url'] = music.audio_url
    ret['title'] = music.M_title
    return ret    


@auth.route('/play/<path:index>',methods=['GET'])
def play(index):
    youtube_urls = get_URL_from_index(index)

    ydl_opts = {
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'webm',
            'preferredquality': '192',
        }],
    }

    info_list = []
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        for youtube_url in youtube_urls:
            info = ydl.extract_info(youtube_url, download=False)
            print()
            info_list.append(info)

    playlist_data = []
    for info in info_list:
        title = info['title']
        artist = info['uploader']
        audio_url = info['url']
        thumbnail_url = max(info['thumbnails'], key=lambda x: x['preference'])['url']
        playlist_data.append({'title': title, 'artist': artist, 'audio_url': audio_url, 'thumbnail_url': thumbnail_url})

    return render_template('play.html', playlist_data=playlist_data, user = current_user)

@auth.route("/creat_playlist", methods=['POST'])
def creat_playlist():
	if request.method == 'POST':
		playlist_name = request.form.get('name')
		playlist_type = request.form.get('type')
		if playlist_name:
			new_playlist = PlayList(P_title=playlist_name, P_type=playlist_type, UID=current_user.UID)
			db.session.add(new_playlist)
			db.session.commit()
			flash("Playlist created successfully!", category="success")
			return new_playlist.P_id
		else:
			flash("Playlist name cannot be empty", category="error")

@auth.route("/add_music_to_playlist", method=['POST'])
def add_music_to_playlist():
	if request.method == 'POST':
		which_playlist_id = request.form.get('playlist_id')
		which_music_id = request.form.get('music_id')
		if which_music_id and which_playlist_id:
			new_music_added_to_playlist = InWhichPlaylist(M_id=which_music_id, P_id=which_playlist_id, UID=current_user.UID)
			db.session.add(new_music_added_to_playlist)
			db.session.commit()
			flash("music added successfully!", category="success")
			return "success"
		else:
			flash("music id or playlist id can't be empty", category="error")
			return "error"

@auth.route("/remove_music_from_playlist", method['POST'])
def remove_music_from_playlist():
	if request.form.method == "POST":
		Which_music_to_remove = request.form.get('music_id')
		Which_playlist = request.form.get('playlist_id')
		if Which_playlist and Which_music_to_remove:
			obj = InWhichPlaylist(P_id=Which_playlist, M_id=Which_music_to_remove, UID=current_user.UID)
			is_exist = InWhichPlaylist.query.filter_by(P_id=Which_playlist, M_id=Which_music_to_remove, UID=current_user.UID).first()
			if not is_exist:
				flash("the object does not exist", category="error")
				return "error"
			db.session.delete(obj)
			db.commit()
			flash("music removed successfully!", category='success')
			return "success"
		else:
			flash("music id or playlist id can not be empty and the chosen music id must include in playlist", category="error")
			return "error"
