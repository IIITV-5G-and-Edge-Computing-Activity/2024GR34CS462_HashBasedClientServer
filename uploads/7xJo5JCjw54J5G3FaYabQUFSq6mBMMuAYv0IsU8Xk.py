import requests

url = "http://127.0.0.1:5000/upload?hash=yourfilehash"
file_path = "C:/Users/sarah/OneDrive/Documents/default_file.txt"

with open(file_path, 'rb') as file:
    files = {'file': file}
    response = requests.post(url, files=files)

print(response.status_code)
print(response.json())
