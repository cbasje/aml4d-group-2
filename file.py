import os

# Set the paths to the directories where the files are stored
INPUT_PATH = "data/input"
OUTPUT_PATH = "data/output"
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}


# Get the data from a file in INPUT_PATH
def read_file(file):
  print(f"Reading '{file}'")
  with open(os.path.join(INPUT_PATH, file), "rb") as f:
    data = f.read()
  return data


# Get all files in a folder
def read_folder(folder):
  files = os.listdir(folder)
  print(f"{len(files)} files in '{folder}'")
  return files


# Check outersection of two lists
def outersection(lst1, lst2):
  temp = set(lst2)
  lst3 = [value for value in lst1 if value not in temp]
  print(lst3)
  return lst3


# Get all images that are not yet used in object_detection (i.e. present in INPUT_PATH but not in OUTPUT_PATH)
def get_unused_files():
  input_files = os.listdir(INPUT_PATH)
  output_files = os.listdir(OUTPUT_PATH)
  files = outersection(input_files, output_files)
  print(f"{len(files)} files unused")
  return files


# Even though the frontend defines this as well, check if the file extension is allowed
def allowed_file(filename):
  return '.' in filename and \
         filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
