import os
import io
from flask import Flask, flash, request, redirect, url_for, send_from_directory, render_template
from werkzeug.utils import secure_filename
import object_detection
import image_classification
import image_coordinates
from file import INPUT_PATH, OUTPUT_PATH, allowed_file, read_folder
from PIL import Image

# Inspired by: https://ask.replit.com/t/how-to-upload-files/14269/2
app = Flask(__name__)
app.config['SECRET_KEY'] = os.urandom(12).hex()

# Set the path to the directory where the files are uploaded
app.config['UPLOAD_FOLDER'] = INPUT_PATH

# Set the maximum file size (in bytes) that is allowed
MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16 MB
app.config['MAX_CONTENT_LENGTH'] = MAX_CONTENT_LENGTH


# Defines the endpoint for the upload/index route
@app.route('/')
def index():
  return render_template('index.html')


# Defines the endpoint to run the image classification function
# Also outputs the results of the function
@app.route('/image-class')
def image_class():
  try:
    table = image_classification.main()
    return render_template('image-class.html', table=table)
  except Exception as e:
    flash('Something went wrong!', "error")
    print(e)
    return render_template('image-class.html')


# Defines the endpoint to run the object detection function
# Also outputs the results of the function
@app.route('/object-det')
def object_det():
  try:
    # Check if calculation should be redone
    redo = request.args.get("redo", type=bool)
    data = object_detection.main(redo)
    return render_template('object-det.html', data=data)
  except Exception as e:
    flash('Something went wrong!', "error")
    print(e)
    return render_template('object-det.html')


# Defines the endpoint to run the image coordinates function
# Also outputs the results of the function
@app.route('/image-coord')
def image_coord():
  try:
    # Check if the object detection stats should be included (and calculated again)
    include_stats = request.args.get("include_stats", type=bool)
    table = image_coordinates.main(include_stats)
    return render_template('image-coord.html', table=table)
  except Exception as e:
    flash('Something went wrong!', "error")
    print(e)
    return render_template('image-coord.html')


# Defines the endpoint where images are uploaded
@app.route('/upload', methods=['POST'])
def upload():
  # Check if files are submitted
  if 'file' not in request.files:
    flash('No file part', "error")
    return redirect('/')

  # Get the list of files
  files = request.files.getlist("file")

  for file in files:
    # If the user does not select a file, the browser submits an empty file without a filename
    if file.filename == '':
      flash('No selected file', "error")
      return redirect('/')

    if file and allowed_file(file.filename):
      # Create an PIL.Image from the submitted file
      img = Image.open(file)

      # Get the EXIF metadata from the PIL.Image (to be used later for image_coordinates)
      exif = None
      if 'exif' in img.info:
        exif = img.info['exif']

      # Check if the PIL.Image is larger than the maximum size
      maxsize = 640
      if img.width > maxsize or img.height > maxsize:
        # Calculate the scale factor to keep aspect ratio
        factor = maxsize / img.height if img.height > img.width else maxsize / img.width
        # Resize the PIL.Image
        img = img.resize((int(img.width * factor), int(img.height * factor)),
                         Image.LANCZOS)

      # Make sure the filename is not dangerous
      filename = secure_filename(file.filename)

      # Save the Image the UPLOAD_FOLDER directory (preferably with the EXIF metadata)
      if exif is not None:
        img.save(os.path.join(app.config['UPLOAD_FOLDER'], filename),
                 exif=exif)
      else:
        img.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

      flash(f"File '{filename}' uploaded successfully", "success")
    else:
      flash(f"Invalid file type for {file.filename}", "error")
  return redirect('/')


# Define the endpoints to serve the files in the input and output directories
@app.route('/files/<string:folder>')
@app.route('/files/<string:folder>/<string:name>')
def get_files(folder, name=None):
  path = f'data/{folder}'
  # Render a single image if name is present, otherwise an HTML page with all images listed
  if name is not None:
    return send_from_directory(path, name)
  else:
    files = read_folder(path)
    return render_template('files.html', folder=folder, files=files)


app.run(host='0.0.0.0', port=81, debug=True)
