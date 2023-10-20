import os
from PIL import Image, ImageOps, ImageDraw, ImageFont
from api import API_OBJECT_DETECTION_URL, request
from file import readFile, readInputFolder

INPUT_PATH = "data/input"
OUTPUT_PATH = "data/output"

label_colors = {
    "bicycle": "orange",
    "car": "red",
    "truck": "red",
    "train": "blue",
    "person": "purple"
}


def drawRectangles(file, data):
  stats = {
      "bicycle": 0,
      "car": 0,
      "truck": 0,
      "train": 0,
  }

  img = Image.open(os.path.join(INPUT_PATH, file))
  img = ImageOps.exif_transpose(img)
  imgDraw = ImageDraw.Draw(img)

  fontHeight = 16
  font = ImageFont.truetype('static/FixelText-SemiBold.ttf', fontHeight)

  outlineWidth = 4

  for i, obj in enumerate(data):
    # print(i, obj['label'])

    if obj['label'] in stats:
      stats[obj['label']] += 1

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

  return stats


def main():
  output = []
  files = readInputFolder()
  for file in files:
    fileData = readFile(file)
    jsonData = request(API_OBJECT_DETECTION_URL, fileData)
    stats = drawRectangles(file, jsonData)
    output.append({"file": file, "stats": stats})

  return output


if __name__ == "__main__":
  main()
