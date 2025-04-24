import requests

url = "http://127.0.0.1:5000/upload?hash=yourfilehash"
file_path = file_path = r"C:\Users\sarah\Downloads\deduplication-system\default_file.py"


with open(file_path, 'rb') as file:
    files = {'file': file}
    response = requests.post(url, files=files)

print(response.status_code)
print(response.text)  # <- this will show the actual HTML or error message from the server

