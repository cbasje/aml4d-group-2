import os

input_path = "data/input"
output_path = "data/output"


def readFile(file):
  print(f"Reading '{file}'")
  with open(os.path.join(input_path, file), "rb") as f:
    data = f.read()
  return data


def readInputFolder():
  files = os.listdir(input_path)
  print(f"{len(files)} files in '{input_path}'")
  return files
