import os
from PIL import Image, ImageOps, ImageDraw, ImageFont
from api import API_OBJECT_DETECTION_URL, request
from file import read_file, read_folder, get_unscanned_files

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


def draw_rectangles(file, data):
  stats = {"bicycle": 0, "car": 0, "truck": 0, "train": 0, "motorcycle": 0}

  img = Image.open(os.path.join(INPUT_PATH, file))

  # This fixes an issue with JPEG images: https://github.com/python-pillow/Pillow/issues/4703
  if 'exif' in img.info:
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


def main(files):
  output = []
  # files = read_folder(INPUT_PATH)
  files = get_unscanned_files()

  for file in files:
    fileData = read_file(file)
    jsonData = request(API_OBJECT_DETECTION_URL, fileData)
    stats = draw_rectangles(file, jsonData)
    output.append({"file": file, "data": jsonData, "stats": stats})

  # df = pd.DataFrame(output)
  # df.to_csv(os.path.join(OUTPUT_PATH, 'obj_detect.csv'))

  return output


if __name__ == "__main__":
  main()
