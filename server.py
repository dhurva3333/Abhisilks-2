from flask import Flask, request, send_from_directory, jsonify
from flask_cors import CORS
import os

app = Flask(__name__)
CORS(app)

IMAGE_FOLDER = 'images'
os.makedirs(IMAGE_FOLDER, exist_ok=True)

@app.route('/upload', methods=['POST'])
def upload_images():
    if 'images' not in request.files:
        return 'No file part', 400
    files = request.files.getlist('images')
    for file in files:
        filepath = os.path.join(IMAGE_FOLDER, file.filename)
        file.save(filepath)
    return 'Upload successful', 200

@app.route('/images')
def get_images():
    files = os.listdir(IMAGE_FOLDER)
    return jsonify(files)

@app.route('/images/<filename>')
def serve_image(filename):
    return send_from_directory(IMAGE_FOLDER, filename)

@app.route('/delete/<filename>', methods=['DELETE'])
def delete_image(filename):
    path = os.path.join(IMAGE_FOLDER, filename)
    if os.path.exists(path):
        os.remove(path)
        return 'Deleted', 200
    return 'Not Found', 404

if __name__ == '__main__':
    app.run(debug=True)
