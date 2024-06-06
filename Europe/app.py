from flask import Flask, request, render_template
import os
import csv
from PIL import Image
from exif import Image as ExifImage
from werkzeug.urls import url_unquote as url_quote

app = Flask(__name__)

UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'jpg', 'jpeg'}

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def get_gps_coordinates(exif_data):
    try:
        if exif_data.has_exif:
            gps_info = exif_data.gps_info
            lat = gps_info.get("GPSLatitude")
            lon = gps_info.get("GPSLongitude")
            lat_ref = gps_info.get("GPSLatitudeRef")
            lon_ref = gps_info.get("GPSLongitudeRef")

            if lat and lon and lat_ref and lon_ref:
                lat = convert_to_degrees(lat)
                lon = convert_to_degrees(lon)
                if lat_ref != "N":
                    lat = -lat
                if lon_ref != "E":
                    lon = -lon
                return lat, lon
    except Exception as e:
        print(f"Error getting GPS coordinates: {e}")
    return None, None

def convert_to_degrees(value):
    d = value[0]
    m = value[1]
    s = value[2]
    return d + (m / 60.0) + (s / 3600.0)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'photo' not in request.files:
        return 'No file part'
    file = request.files['photo']
    if file.filename == '':
        return 'No selected file'
    if file and allowed_file(file.filename):
        filename = file.filename
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(file_path)
        with open(file_path, 'rb') as image_file:
            image = ExifImage(image_file)
            lat, lon = get_gps_coordinates(image)
            if lat and lon:
                with open('output.csv', 'a', newline='') as csvfile:
                    csvwriter = csv.writer(csvfile)
                    csvwriter.writerow([filename, lat, lon])
        return 'File uploaded successfully'
    else:
        return 'Invalid file format'

if __name__ == '__main__':
    app.run(debug=True)
