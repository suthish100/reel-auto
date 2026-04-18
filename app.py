from flask import Flask, request, jsonify, send_from_directory
import subprocess
import uuid
import os

app = Flask(__name__)

DOWNLOAD_FOLDER = "static"
os.makedirs(DOWNLOAD_FOLDER, exist_ok=True)

@app.route("/download", methods=["POST"])
def download():
    data = request.json
    reel_url = data.get("url")

    filename = f"{uuid.uuid4()}.mp4"
    filepath = os.path.join(DOWNLOAD_FOLDER, filename)

    subprocess.run([
        "yt-dlp",
        "-o", filepath,
        reel_url
    ])

    return jsonify({
        "video_url": request.host_url + "files/" + filename
    })

@app.route("/files/<filename>")
def files(filename):
    return send_from_directory(DOWNLOAD_FOLDER, filename)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
