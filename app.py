from flask import Flask, request, jsonify, send_from_directory
import subprocess
import uuid
import os

app = Flask(__name__)

DOWNLOAD_FOLDER = "downloads"
os.makedirs(DOWNLOAD_FOLDER, exist_ok=True)

@app.route("/download", methods=["POST"])
def download():
    data = request.json
    reel_url = data.get("url")

    unique_id = str(uuid.uuid4())
    output_template = os.path.join(DOWNLOAD_FOLDER, f"{unique_id}.%(ext)s")

    result = subprocess.run(
        [
            "yt-dlp",
            "-f", "mp4",
            "-o", output_template,
            reel_url
        ],
        capture_output=True,
        text=True
    )

    # Find the downloaded file
    files = [f for f in os.listdir(DOWNLOAD_FOLDER) if f.startswith(unique_id)]

    if not files:
        return jsonify({
            "error": "Download failed",
            "details": result.stderr
        }), 500

    filename = files[0]

    return jsonify({
        "video_url": request.host_url + "files/" + filename
    })

@app.route("/upload-temp", methods=["POST"])
def upload_temp():
    print("FILES:", request.files)

    if "file" not in request.files:
        return jsonify({
            "error": "No file uploaded",
            "received_files": list(request.files.keys()),
            "content_type": request.content_type
        }), 400

    uploaded_file = request.files["file"]

    filename = f"{uuid.uuid4()}.mp4"
    filepath = os.path.join(DOWNLOAD_FOLDER, filename)

    uploaded_file.save(filepath)

    return jsonify({
        "video_url": request.host_url + "files/" + filename
    })
@app.route("/files/<filename>")
def files(filename):
   return send_from_directory('downloads', filename, as_attachment=False)
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
