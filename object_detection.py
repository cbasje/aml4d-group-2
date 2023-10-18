import os
from PIL import Image, ImageDraw, ImageFont
from pillow_heif import register_heif_opener
from api import API_OBJECT_DETECTION_URL, request
from file import readFile, readInputFolder

input_path = "data/input"
output_path = "data/output"

label_colors = {
    "bicycle": "orange",
    "car": "red",
    "truck": "red",
    "person": "purple"
}


def get_exif(file):
  img = Image.open(os.path.join(input_path, file))
  img.verify()
  return img.getexif().get_ifd(0x8825)


def get_geotagging(exif):
  geo_tagging_info = {}
  if not exif:
    raise ValueError("No EXIF metadata found")
  else:
    gps_keys = [
        'GPSVersionID', 'GPSLatitudeRef', 'GPSLatitude', 'GPSLongitudeRef',
        'GPSLongitude', 'GPSAltitudeRef', 'GPSAltitude', 'GPSTimeStamp',
        'GPSSatellites', 'GPSStatus', 'GPSMeasureMode', 'GPSDOP',
        'GPSSpeedRef', 'GPSSpeed', 'GPSTrackRef', 'GPSTrack',
        'GPSImgDirectionRef', 'GPSImgDirection', 'GPSMapDatum',
        'GPSDestLatitudeRef', 'GPSDestLatitude', 'GPSDestLongitudeRef',
        'GPSDestLongitude', 'GPSDestBearingRef', 'GPSDestBearing',
        'GPSDestDistanceRef', 'GPSDestDistance', 'GPSProcessingMethod',
        'GPSAreaInformation', 'GPSDateStamp', 'GPSDifferential'
    ]

    for k, v in exif.items():
      try:
        geo_tagging_info[gps_keys[k]] = str(v)
      except IndexError:
        pass
    return geo_tagging_info


def drawRectangles(file, data):
  img = Image.open(os.path.join(input_path, file))
  img.verify()

  imgDraw = ImageDraw.Draw(img)

  fontHeight = 16
  font = ImageFont.truetype('assets/FixelText-SemiBold.ttf', fontHeight)

  outlineWidth = 4

  for i, obj in enumerate(data):
    print(i, obj['label'])

    box = obj['box']
    color = label_colors.get(obj['label'], "black")

    labelLength = font.getlength(obj['label'])
    labelBgShape = [
        box['xmin'] + outlineWidth, box['ymin'],
        box['xmin'] + labelLength + (outlineWidth * 2),
        box['ymin'] + fontHeight + outlineWidth
    ]
    imgDraw.rectangle(labelBgShape, fill=color, outline=None)
    imgDraw.text((box['xmin'] + outlineWidth, box['ymin']),
                 obj['label'],
                 fill="white",
                 font=font)

    outlineShape = [box['xmin'], box['ymin'], box['xmax'], box['ymax']]
    imgDraw.rectangle(outlineShape,
                      fill=None,
                      outline=color,
                      width=outlineWidth)

  img.save(os.path.join(output_path, file))


def main():
  register_heif_opener()

  files = readInputFolder()
  for file in files[:1]:
    # fileData = readFile(file)
    # jsonData = request(API_OBJECT_DETECTION_URL, fileData)

    image_info = get_exif('IMG_2054.HEIC')
    results = get_geotagging(image_info)
    print(results)
    # drawRectangles(file, jsonData)
