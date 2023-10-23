import os
from PIL import Image, ImageOps, ImageDraw, ImageFont
from api import API_OBJECT_DETECTION_URL, request
from file import read_file, read_folder

INPUT_PATH = "data/input"
OUTPUT_PATH = "data/output"

label_colors = {
    "bicycle": "orange",
    "car": "red",
    "truck": "red",
    "train": "blue",
    "person": "purple",
    "motorcycle": "blueviolet"
}


# Check outersection of two lists
def outersection(lst1, lst2):
  temp = set(lst2)
  lst3 = [value for value in lst1 if value not in temp]
  return lst3


def drawRectangles(file, data):
  stats = {"bicycle": 0, "car": 0, "truck": 0, "train": 0, "motorcycle": 0}

  img = Image.open(os.path.join(INPUT_PATH, file))

  # This fixes an issue with JPEG images: https://github.com/python-pillow/Pillow/issues/4703
  img = ImageOps.exif_transpose(img)

  imgDraw = ImageDraw.Draw(img)

  fontHeight = 8
  font = ImageFont.truetype('static/FixelText-Bold.ttf', fontHeight)

  outlineWidth = 4

  for i, obj in enumerate(data):
    # print(i, obj['label'], obj)

    if obj['label'] in stats:
      stats[obj['label']] += 1

    box = obj['box']
    color = label_colors.get(obj['label'], "black")
    label = f"{obj['label']} ({round(obj['score'], 3)})"

    labelLength = font.getlength(label)
    labelBgShape = [
        box['xmin'] + outlineWidth, box['ymin'],
        box['xmin'] + labelLength + (outlineWidth * 2),
        box['ymin'] + fontHeight + (outlineWidth * 2)
    ]
    imgDraw.rectangle(labelBgShape, fill=color, outline=None)
    imgDraw.text((box['xmin'] + outlineWidth, box['ymin'] + outlineWidth),
                 label,
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
  input_files = read_folder(INPUT_PATH)
  output_files = read_folder(OUTPUT_PATH)
  for file in outersection(input_files, output_files):
    fileData = read_file(file)
    jsonData = request(API_OBJECT_DETECTION_URL, fileData)
    stats = drawRectangles(file, jsonData)
    output.append({"file": file, "data": jsonData, "stats": stats})

  return output


if __name__ == "__main__":
  main()
