import os

INPUT_PATH = "data/input"
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}


def read_file(file):
  print(f"Reading '{file}'")
  with open(os.path.join(INPUT_PATH, file), "rb") as f:
    data = f.read()
  return data


def read_folder(folder):
  files = os.listdir(folder)
  print(f"{len(files)} files in '{folder}'")
  return files


def allowed_file(filename):
  return '.' in filename and \
         filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
