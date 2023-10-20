import os

INPUT_PATH = "data/input"
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

def readFile(file):
  print(f"Reading '{file}'")
  with open(os.path.join(INPUT_PATH, file), "rb") as f:
    data = f.read()
  return data


def readInputFolder():
  files = os.listdir(INPUT_PATH)
  print(f"{len(files)} files in '{INPUT_PATH}'")
  return files

def allowed_file(filename):
  return '.' in filename and \
         filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS