from flask import Flask, request, redirect, url_for, render_template, send_from_directory
import os
import subprocess
from datetime import datetime

app = Flask(__name__)
UPLOAD_FOLDER = 'static/videos'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload():
    files = [request.files.get(f'foto{i}') for i in range(1, 4)]
    filenames = []
    timestamp = datetime.now().strftime('%Y%m%d%H%M%S')

    temp_dir = f'temp_{timestamp}'
    os.makedirs(temp_dir, exist_ok=True)

    for i, file in enumerate(files):
        if file:
            filename = f'{temp_dir}/img{i}.jpg'
            file.save(filename)
            filenames.append(filename)

    list_file_path = f'{temp_dir}/list.txt'
    with open(list_file_path, 'w') as f:
        for file in filenames:
            f.write(f"file '{file}'\n")
            f.write("duration 2\n")
        f.write(f"file '{filenames[-1]}'\n")  # last frame holds

    output_path = f'{UPLOAD_FOLDER}/video_{timestamp}.mp4'
    command = [
        'ffmpeg',
        '-f', 'concat',
        '-safe', '0',
        '-i', list_file_path,
        '-vsync', 'vfr',
        '-pix_fmt', 'yuv420p',
        output_path
    ]
    subprocess.run(command)

    return redirect(url_for('index', video=url_for('static', filename=f'videos/video_{timestamp}.mp4')))

