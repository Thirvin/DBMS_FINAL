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

