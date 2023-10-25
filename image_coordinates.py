import os
import re
import ast
from PIL import Image, ExifTags
from file import INPUT_PATH, OUTPUT_PATH, read_folder
import pandas as pd


# Parse the Minute/Second format of the coordinates into Decimal format
# This function is inspired by: https://stackoverflow.com/questions/33997361/how-to-convert-degree-minute-second-to-degree-decimal
def parse_coords(tuple, direction):
  coordString = f"""{tuple[0]}°{tuple[1]}'{tuple[2]}"{direction}"""
  deg, minutes, seconds, direction = re.split('[°\'"]', coordString)
  return (float(deg) + float(minutes) / 60 + float(seconds) /
          (60 * 60)) * (-1 if direction in ['W', 'S'] else 1)


# Get the EXIF metadate for an image in INPUT_PATH
def get_exif(file):
  img = Image.open(os.path.join(INPUT_PATH, file))
  return img.getexif().get_ifd(ExifTags.IFD.GPSInfo)


# Get the geotagging information for an image
# This function is inspired by the PIL/Pillow documentation: https://pillow.readthedocs.io/en/stable/reference/Image.html#PIL.Image.Exif
def get_geotagging(file, stats={}):
  # The statistics coming from the object_det.csv file is a <str>, so parse into a <dict>
  stats = ast.literal_eval(stats)
  
  image_exif = get_exif(file)

  if not image_exif:
    # If there is no EXIF, continue to the next file
    print(f"'{file}' has no exif data.")
    return pd.Series({
        "file": file,
        "latitude": None,
        "longitude": None,
        **stats
    })
  else:
    # for key, val in image_exif.items():
    #   if key in ExifTags.GPSTAGS:
    #     print(f'{ExifTags.GPSTAGS[key]}:{val}')

    # Create a new pandas Series for the file with the geotagging information (+ pre-existing statistics)
    return pd.Series({
        "file":
        file,
        "latitude":
        parse_coords(image_exif[ExifTags.GPS.GPSLatitude],
                     image_exif[ExifTags.GPS.GPSLatitudeRef]),
        "longitude":
        parse_coords(image_exif[ExifTags.GPS.GPSLongitude],
                     image_exif[ExifTags.GPS.GPSLongitudeRef]),
        **stats
    })


def main(include_stats=False):
  if include_stats:
    # If the object detection statistics should be included, read it from the obj_detect.csv file
    files = pd.read_csv(os.path.join(OUTPUT_PATH, 'obj_detect.csv'))
    df = pd.DataFrame([
        get_geotagging(file['file'], file['stats'])
        for i, file in files.iterrows()
    ])
  else:
    # If no statistics should be included, get files from INPUT_PATH
    files = read_folder(INPUT_PATH)
    df = pd.DataFrame([get_geotagging(file) for file in files])

  # Generate (and save) a CSV file from the Dataframe
  df.to_csv(os.path.join(OUTPUT_PATH, "image_coordinates.csv"))

  # Generate an HTML table from the Dataframe
  return df.to_html()


if __name__ == "__main__":
  main()
