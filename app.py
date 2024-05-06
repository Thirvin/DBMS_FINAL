from flask import Flask, render_template, request, send_file
import subprocess
import yt_dlp
app = Flask(__name__)

DOWNLOADS_FOLDER = 'downloads'

@app.route('/')
def index():
    return render_template('index.html')
@app.route('/download_music', methods=['POST'])
def download_music():
    url = request.form['url']
    
    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': f'{DOWNLOADS_FOLDER}/%(title)s.%(ext)s',
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=True)
    
    return "Music downloaded successfully!"
@app.route('/search', methods=['GET', 'POST'])
def search():
    if request.method == 'POST':
        query = request.form['query']
        search_command = ['youtube-dl', '-x', '--audio-format', 'mp3', '-o', f'{DOWNLOADS_FOLDER}/%(title)s.%(ext)s', f'ytsearch:"{query}"']
        subprocess.run(search_command)
        music_files = subprocess.run(['ls', DOWNLOADS_FOLDER], capture_output=True, text=True).stdout.split('\n')
        music_files = [file for file in music_files if file]
        search_results = [{"title": file.split('.')[0], "url": f"/play/{i}"} for i, file in enumerate(music_files)]
        return render_template('search_results.html', query=query, search_results=search_results)
    else:
        return render_template('search.html')
from flask import send_file

@app.route('/play/<path:music_file>')
def play(music_file):
    return send_file(DOWNLOADS_FOLDER+'/'+music_file, as_attachment=False)

if __name__ == '__main__':
    app.run(debug=True)

