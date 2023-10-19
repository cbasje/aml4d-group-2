import os

INPUT_PATH = "data/input"


def readFile(file):
  print(f"Reading '{file}'")
  with open(os.path.join(INPUT_PATH, file), "rb") as f:
    data = f.read()
  return data


def readInputFolder():
  files = os.listdir(INPUT_PATH)
  print(f"{len(files)} files in '{INPUT_PATH}'")
  return files
