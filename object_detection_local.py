import os
import torch
import pandas as pd
from PIL import Image, ImageOps, ImageDraw, ImageFont
from file import INPUT_PATH, OUTPUT_PATH, read_folder, get_unused_files

# Model
model = torch.hub.load('ultralytics/yolov5', 'yolov5s', pretrained=True)

# Define the settings for bounding boxes
fontHeight = 8
font = ImageFont.truetype('static/FixelText-Bold.ttf', fontHeight)

outlineWidth = 4

# Define colors for some classes for human readability
label_colors = {
    "bicycle": "orange",
    "car": "red",
    "truck": "red",
    "train": "blue",
    "person": "purple",
    "motorcycle": "blueviolet"
}


def draw_rectangles(file, data):
  # Start a new object to collect statistics for each file
  stats = {"bicycle": 0, "car": 0, "truck": 0, "train": 0, "motorcycle": 0}

  # Create an PIL.Image from the original image in INPUT_PATH
  img = Image.open(os.path.join(INPUT_PATH, file))

  # This fixes an issue with the orientation of JPEG images: https://github.com/python-pillow/Pillow/issues/4703
  # Without this, it would keep portrait images in landscape and draw bounding boxes incorrectly
  if 'exif' in img.info:
    img = ImageOps.exif_transpose(img)

  # Create drawing object for the current image
  imgDraw = ImageDraw.Draw(img)

  for i, obj in data.iterrows():
    # Track the statistics
    if obj['name'] in stats:
      stats[obj['name']] += 1

    color = label_colors.get(obj['name'], "black")
    label = f"{obj['name']} ({round(obj['confidence'], 3)})"

    # Draw a box around/behind the label (+ score)
    labelLength = font.getlength(label)
    labelBgShape = [
        obj['xmin'] + outlineWidth, obj['ymin'],
        obj['xmin'] + labelLength + (outlineWidth * 2),
        obj['ymin'] + fontHeight + (outlineWidth * 2)
    ]
    imgDraw.rectangle(labelBgShape, fill=color, outline=None)

    # Draw the label (+ score)
    imgDraw.text((obj['xmin'] + outlineWidth, obj['ymin'] + outlineWidth),
                 label,
                 fill="white",
                 font=font)

    # Draw the bounding box
    outlineShape = [obj['xmin'], obj['ymin'], obj['xmax'], obj['ymax']]
    imgDraw.rectangle(outlineShape,
                      fill=None,
                      outline=color,
                      width=outlineWidth)

  # Save the new image to OUTPUT_PATH
  img.save(os.path.join(OUTPUT_PATH, file))
  print(f"'{file}' has {len(data)} objects")

  # Output the statistics for the current image
  return stats


def main():
  output = []
  files = read_folder(INPUT_PATH)
#   files = get_unused_files()

  # Get the data from the Hugging Face API for each file and draw the bounding boxes
  for file in files:
    print(f"Reading '{file}'")
    results = model([os.path.join(INPUT_PATH, file)])
    stats = draw_rectangles(file, results.pandas().xyxy[0])
    output.append({"file": file, "data": results.pandas().xyxy, "stats": stats})

  # Generate (and save) a CSV file from the Dataframe
  # df = pd.DataFrame(output)
  # df.to_csv(os.path.join(OUTPUT_PATH, 'obj_detect.csv'))

  # Output the data to use in the HTML page
  return output


if __name__ == "__main__":
  main()