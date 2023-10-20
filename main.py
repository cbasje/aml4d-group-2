import os
from flask import Flask, flash, request, redirect, url_for, send_from_directory, render_template
from werkzeug.utils import secure_filename
import object_detection
import image_classification
import image_coordinates
from file import allowed_file

# Inspired by: https://ask.replit.com/t/how-to-upload-files/14269/2
app = Flask(__name__)
app.config['SECRET_KEY'] = os.urandom(12).hex()

# Set the path to the directory where you want to store the uploaded files
INPUT_PATH = "data/input"
OUTPUT_PATH = "data/output"

# Set the maximum file size (in bytes) that you want to allow
MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16 MB

app.config['UPLOAD_FOLDER'] = INPUT_PATH
app.config['MAX_CONTENT_LENGTH'] = MAX_CONTENT_LENGTH


@app.route('/')
def index():
  return render_template('index.html')


@app.route('/image-class')
def image_class():
  try:
    table = image_classification.main()
    return render_template('image-class.html', table=table)
  except:
    flash('Something went wrong!', "error")
    return render_template('image-class.html')


@app.route('/object-det')
def object_det():
  try:
    data = object_detection.main()
    return render_template('object-det.html', data=data)
  except:
    flash('Something went wrong!', "error")
    return render_template('object-det.html')


@app.route('/image-coord')
def image_coord():
  try:
    table = image_coordinates.main()
    return render_template('image-coord.html', table=table)
  except:
    flash('Something went wrong!', "error")
    return render_template('image-coord.html')


@app.route('/upload', methods=['POST'])
def upload():
  # Check if the post request has the file part
  if 'file' not in request.files:
    flash('No file part', "error")
    return redirect('/')

  # Get the list of files
  files = request.files.getlist("file")

  # Iterate for each file in the files List, and Save them
  for file in files:
    # If the user does not select a file, the browser submits an empty file without a filename
    if file.filename == '':
      flash('No selected file', "error")
      return redirect('/')

    if file and allowed_file(file.filename):
      filename = secure_filename(file.filename)
      # Save the uploaded file to the UPLOAD_FOLDER directory
      file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
      flash(f"File {filename} uploaded successfully", "success")
    else:
      flash(f"Invalid file type for {file.filename}", "error")
  return redirect('/')


@app.route('/output-files/<name>')
def download_file(name):
  return send_from_directory(OUTPUT_PATH, name)


app.add_url_rule("/output-files/<name>",
                 endpoint="download_file",
                 build_only=True)

app.run(host='0.0.0.0', port=81, debug=True)
