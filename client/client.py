import requests
import hashlib
import sys
import os

def sarah_hash_file(filepath):
    # Compute and return the SHA256 hash of the given file
    sha = hashlib.sha256()
    with open(filepath, 'rb') as f:
        while chunk := f.read(8192):
            sha.update(chunk)
    return sha.hexdigest()

def sarah_upload_file(filepath):
    file_hash = sarah_hash_file(filepath)
    files = {'file': open(filepath, 'rb')}
    response = requests.post(f"http://server:5000/upload?hash={file_hash}", files=files)
    print(response.json())

if __name__ == "__main__":
    sarah_upload_file(sys.argv[1])
