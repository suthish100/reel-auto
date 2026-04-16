from flask import Flask, request, jsonify
import subprocess
import uuid
import os

app = Flask(__name__)

@app.route("/download", methods=["POST"])
def download():
    data = request.json
    reel_url = data.get("url")

    filename = f"{uuid.uuid4()}.mp4"

    command = [
        "yt-dlp",
        "-o", filename,
        reel_url
    ]

    subprocess.run(command)

    return jsonify({
        "file": filename
    })

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
