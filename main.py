import os
from flask import Flask, flash, request, redirect, url_for, send_from_directory, render_template
from werkzeug.utils import secure_filename
import object_detection
import image_classification
import image_coordinates

# Inspired by: https://ask.replit.com/t/how-to-upload-files/14269/2
app = Flask(__name__)
app.config['SECRET_KEY'] = os.urandom(12).hex()

# Set the path to the directory where you want to store the uploaded files
UPLOAD_PATH = "data/input"

# Set the allowed file extensions
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

# Set the maximum file size (in bytes) that you want to allow
MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16 MB

app.config['UPLOAD_FOLDER'] = UPLOAD_PATH
app.config['MAX_CONTENT_LENGTH'] = MAX_CONTENT_LENGTH


# Define a function to check if the file extension is allowed
def allowed_file(filename):
  return '.' in filename and \
         filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/')
def index():
  return render_template('index.html')


@app.route('/image-class')
def image_class():
  image_classification.main()
  return redirect('/')


@app.route('/object-det')
def object_det():
  object_detection.main()
  return redirect('/')


@app.route('/image-coord')
def image_coord():
  image_coordinates.main()
  return redirect('/')


@app.route('/upload', methods=['POST'])
def upload():
  # Check if the post request has the file part
  if 'file' not in request.files:
    flash('No file part')
    return redirect('/')

  # Get the list of files
  files = request.files.getlist("file")

  # Iterate for each file in the files List, and Save them
  for file in files:
    # If the user does not select a file, the browser submits an empty file without a filename
    if file.filename == '':
      flash('No selected file')
      return redirect('/')

    if file and allowed_file(file.filename):
      # Save the uploaded file to the UPLOAD_FOLDER directory
      file.save(os.path.join(app.config['UPLOAD_FOLDER'], file.filename))
      flash(f"File {file.filename} uploaded successfully")
    else:
      flash(f"Invalid file type for {file.filename}")
  return redirect('/')


@app.route('/files/<name>')
def download_file(name):
  return send_from_directory(app.config["UPLOAD_FOLDER"], name)


app.add_url_rule("/files/<name>", endpoint="download_file", build_only=True)

app.run(host='0.0.0.0', port=81, debug=True)
