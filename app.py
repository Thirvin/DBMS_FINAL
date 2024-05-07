from flask import Flask, render_template, request, send_file
import subprocess
import yt_dlp
from flask import send_from_directory
app = Flask(__name__)

DOWNLOADS_FOLDER = 'downloads'
urls = ['https://youtu.be/ovTiSA9T-RU?si=H5r_oO7-tboMBeYB','https://youtu.be/kkUWlcjmOew?si=LYhySQt4XrsUFOxP']
def get_URL_from_index(index):
    return urls[int(index)] 

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/search', methods=['POST'])
def search():
    youtube_url = request.form['youtube_url']
    ydl_opts = {
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'webm',
            'preferredquality': '192',
        }],
    }
    audio_url = ""
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info_dict = ydl.extract_info(youtube_url, download=False)
        audio_url = info_dict['url']

    return render_template('play.html', audio_url=audio_url)

@app.route('/play/<path:index>')
def play(index):
    youtube_url = get_URL_from_index(index)

    ydl_opts = {
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

    return render_template('play.html', audio_url=audio_url)

'''
def play(music_file):
    song = {
        'title': '３月桃花',
        'artist': '珂拉琪 Collage',
        #'url': DOWNLOADS_FOLDER+'/'+music_file+".webm"
        'url' : 'https://youtu.be/ovTiSA9T-RU?si=WnELN2wrWmW-lLlF'
    }
    return render_template('play.html', song=song)
'''
@app.route('/play/downloads/<path:filename>')
def download_file(filename):
    return send_from_directory('downloads', filename)

if __name__ == '__main__':
    app.run(debug=True,host='0.0.0.0')

