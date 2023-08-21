code = '''
from google.colab import files
import os

# Define the target directory
target_directory = '/content/penguins/Test/'

# Create the target directory if it doesn't exist
os.makedirs(target_directory, exist_ok=True)

# Prompt the user to upload files
uploaded = files.upload()

# Access the uploaded files and save to the target directory
for filename, content in uploaded.items():
    target_path = os.path.join(target_directory, filename)
    with open(target_path, 'wb') as f:
        f.write(content)
    print(f"{filename} uploaded and saved to {target_path}.")
'''

with open('/content/upload_files.py', 'w') as f:
    f.write(code)