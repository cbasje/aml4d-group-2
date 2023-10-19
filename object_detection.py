import os
from PIL import Image, ImageDraw, ImageFont
from api import API_OBJECT_DETECTION_URL, request
from file import readFile, readInputFolder

INPUT_PATH = "data/input"
OUTPUT_PATH = "data/output"

label_colors = {
    "bicycle": "orange",
    "car": "red",
    "truck": "red",
    "person": "purple"
}


def drawRectangles(file, data):
  img = Image.open(os.path.join(INPUT_PATH, file))
  imgDraw = ImageDraw.Draw(img)

  fontHeight = 16
  font = ImageFont.truetype('static/FixelText-SemiBold.ttf', fontHeight)

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

  img.save(os.path.join(OUTPUT_PATH, file))
  print(f"'{file}' has {len(data)} objects")


def main():
  files = readInputFolder()
  for file in files:
    fileData = readFile(file)
    jsonData = request(API_OBJECT_DETECTION_URL, fileData)
    drawRectangles(file, jsonData)


if __name__ == "__main__":
  main()
