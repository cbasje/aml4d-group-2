import os
from PIL import Image, ImageDraw, ImageFont
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


def drawRectangles(file, data):
  img = Image.open(os.path.join(input_path, file))
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
  print(f"'{file}' has {len(data)} objects")


def main():
  files = readInputFolder()
  for file in files:
    fileData = readFile(file)
    jsonData = request(API_OBJECT_DETECTION_URL, fileData)
    drawRectangles(file, jsonData)
