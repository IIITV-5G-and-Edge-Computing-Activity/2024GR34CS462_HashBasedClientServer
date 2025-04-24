file_path = 'C:/Users/sarah/Documents/default_file.txt'  

content = '''This is a default file created for testing purposes.
You can modify the content or add more lines as needed.
This file will be used for uploading to the server.
'''

with open(file_path, 'w') as file:
    file.write(content)

print(f"File created at {file_path}")
