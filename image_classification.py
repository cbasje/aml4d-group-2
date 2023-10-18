import os
import pandas as pd
from api import API_IMAGE_CLASSIFICATION_URL, request
from file import readFile, readInputFolder

input_path = "data/input"
output_path = "data/output"


def queryFile(file):
  fileData = readFile(file)
  return request(API_IMAGE_CLASSIFICATION_URL, fileData)


def valuesToRow(values, file):
  row = dict((obj['label'], obj['score']) for obj in values)
  return pd.Series({'file': file} | row)


def main():
  files = readInputFolder()
  data = [queryFile(file) for file in files]
  print(data)

  df = pd.DataFrame([valuesToRow(obj, files[i]) for i, obj in enumerate(data)])
  print(df)

  df.to_csv(os.path.join(output_path, "image_classification.csv"), decimal=",")
