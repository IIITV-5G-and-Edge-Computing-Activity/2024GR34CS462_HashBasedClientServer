from flask import Flask, request, jsonify
import os, json
from flask_cors import CORS  

app = Flask(__name__)
CORS(app)  
app = Flask(__name__)
UPLOAD_FOLDER = './storage/uploads'
METADATA_FILE = './storage/metadata.json'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

if not os.path.exists(METADATA_FILE):
    with open(METADATA_FILE, 'w') as f:
        json.dump({}, f)

@app.route('/upload', methods=['POST'])
def sarah_upload():
    file = request.files['file']
    file_hash = request.args.get('hash')

    with open(METADATA_FILE, 'r') as f:
        metadata = json.load(f)

    if file_hash in metadata:
        return jsonify({'status': 'duplicate', 'message': 'File already exists'}), 200

    save_path = os.path.join(UPLOAD_FOLDER, file.filename)
    file.save(save_path)
    metadata[file_hash] = file.filename

    with open(METADATA_FILE, 'w') as f:
        json.dump(metadata, f)

    return jsonify({'status': 'uploaded', 'message': 'File uploaded successfully'}), 201

if __name__ == '__main__':
    app.run(host='0.0.0.0',debug=True)
