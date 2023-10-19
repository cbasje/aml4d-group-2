import os
import re
from PIL import Image, ExifTags
from file import readFile, readInputFolder
import pandas as pd

INPUT_PATH = "data/input"
OUTPUT_PATH = "data/output"


# This function is inspired by: https://stackoverflow.com/questions/33997361/how-to-convert-degree-minute-second-to-degree-decimal
def parseCoord(tuple, direction):
  coordString = f"""{tuple[0]}°{tuple[1]}'{tuple[2]}"{direction}"""
  deg, minutes, seconds, direction = re.split('[°\'"]', coordString)
  return (float(deg) + float(minutes) / 60 + float(seconds) /
          (60 * 60)) * (-1 if direction in ['W', 'S'] else 1)


def getExif(file):
  img = Image.open(os.path.join(INPUT_PATH, file))
  return img.getexif().get_ifd(ExifTags.IFD.GPSInfo)


# This function is inspired by the Pillow documentation: https://pillow.readthedocs.io/en/stable/reference/Image.html#PIL.Image.Exif
def getGeotagging(file):
  image_exif = getExif(file)

  if not image_exif:
    # raise ValueError("No EXIF metadata found")
    print(f"'{file}' has no exif data.")
    return pd.Series({"file": file, "latitude": None, "longitude": None})
  else:
    for key, val in image_exif.items():
      if key in ExifTags.GPSTAGS:
        print(f'{ExifTags.GPSTAGS[key]}:{val}')

    return pd.Series({
        "file":
        file,
        "latitude":
        parseCoord(image_exif[ExifTags.GPS.GPSLatitude],
                   image_exif[ExifTags.GPS.GPSLatitudeRef]),
        "longitude":
        parseCoord(image_exif[ExifTags.GPS.GPSLongitude],
                   image_exif[ExifTags.GPS.GPSLongitudeRef])
    })


def main():
  # registerHeifOpener()

  files = readInputFolder()
  df = pd.DataFrame([getGeotagging(file) for file in files])
  print(df)

  df.to_csv(os.path.join(OUTPUT_PATH, "image_coordinates.csv"))

  return df.to_html()


if __name__ == "__main__":
  main()
