import os
import pandas as pd
from api import API_IMAGE_CLASSIFICATION_URL, request
from file import INPUT_PATH, OUTPUT_PATH, read_file, read_folder


# Define a reusable function to perform requests to the Hugging Face API on a specific file
def queryFile(file):
  fileData = read_file(file)
  return request(API_IMAGE_CLASSIFICATION_URL, fileData)


# Transform the data from the Hugging Face API for a human readable CSV file/HTML table
def valuesToRow(values, file):
  row = dict((obj['label'], obj['score']) for obj in values)
  return pd.Series({'file': file} | row)


def main():
  files = read_folder(INPUT_PATH)

  # Get the data from the Hugging Face API for each file
  data = [queryFile(file) for file in files]
  df = pd.DataFrame([valuesToRow(obj, files[i]) for i, obj in enumerate(data)])

  # Generate (and save) a CSV file from the Dataframe
  df.to_csv(os.path.join(OUTPUT_PATH, "image_classification.csv"), decimal=",")

  # Generate an HTML table from the Dataframe
  return df.to_html()


if __name__ == "__main__":
  main()
