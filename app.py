from flask import Flask, render_template, request, jsonify, send_from_directory
import os
import hashlib
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__, static_folder='static')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///files.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

UPLOAD_FOLDER = 'uploads'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

class File(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    file_hash = db.Column(db.String(64), unique=True, nullable=False)
    file_path = db.Column(db.String(256), nullable=False)

    def __repr__(self):
        return f"<File {self.file_hash}>"

with app.app_context():
    db.create_all()

@app.route('/')
def serve_index():
    return render_template('index.html')

def calculate_file_hash(file):
    """
    Calculate SHA-256 hash of a file.
    """
    sha256_hash = hashlib.sha256()
    for byte_block in iter(lambda: file.read(4096), b""):
        sha256_hash.update(byte_block)
    return sha256_hash.hexdigest()

@app.route('/upload', methods=['POST'])
def upload_file():
    file = request.files.get('file')

    if not file:
        return jsonify({'status': 'error', 'message': 'No file uploaded'}), 400

    file_hash = calculate_file_hash(file)

    existing_file = File.query.filter_by(file_hash=file_hash).first()

    if existing_file:
        return jsonify({'status': 'duplicate', 'message': 'File already uploaded (duplicate)'}), 200

    file_path = os.path.join(UPLOAD_FOLDER, file_hash)
    file.seek(0)
    file.save(file_path)

    new_file = File(file_hash=file_hash, file_path=file_path)
    db.session.add(new_file)
    db.session.commit()

    return jsonify({'status': 'uploaded', 'message': 'File uploaded successfully'}), 200

@app.route('/upload', methods=['GET'])
def check_file_by_hash():
    file_hash = request.args.get('hash')
    if not file_hash:
        return jsonify({'status': 'error', 'message': 'Missing hash parameter'}), 400

    existing_file = File.query.filter_by(file_hash=file_hash).first()

    if existing_file:
        return jsonify({'status': 'found', 'message': 'File exists'}), 200
    else:
        return jsonify({'status': 'not_found', 'message': 'File not found'}), 404

if __name__ == '__main__':
    app.run(debug=True)
