from flask import Flask, request, render_template
import os
from PIL import Image
import piexif

app = Flask(__name__)

UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'jpg', 'jpeg'}

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def get_gps_coordinates(exif_data):
    gps = exif_data.get('GPS')
    if gps:
        lat = gps.get(piexif.GPSIFD.GPSLatitude)
        lon = gps.get(piexif.GPSIFD.GPSLongitude)
        if lat and lon:
            lat_ref = gps.get(piexif.GPSIFD.GPSLatitudeRef)
            lon_ref = gps.get(piexif.GPSIFD.GPSLongitudeRef)
            lat = convert_to_degrees(lat)
            lon = convert_to_degrees(lon)
            if lat_ref != 'N':
                lat = -lat
            if lon_ref != 'E':
                lon = -lon
            return lat, lon
    return None, None

def convert_to_degrees(value):
    degrees = value[0][0] / value[0][1]
    minutes = value[1][0] / value[1][1]
    seconds = value[2][0] / value[2][1]
    return degrees + minutes / 60 + seconds / 3600

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
        try:
            exif_data = piexif.load(file_path)
            print("Exif Data:", exif_data)  # Log the contents of exif_data
            lat, lon = get_gps_coordinates(exif_data)
            print("GPS Coordinates:", lat, lon)  # Log the extracted GPS coordinates
            if lat is not None and lon is not None:
                return f'File uploaded successfully. GPS Coordinates: {lat}, {lon}'
            else:
                return 'No GPS coordinates found in the photo.'
        except Exception as e:
            return f'Error processing the file: {e}'
    else:
        return 'Invalid file format'

if __name__ == '__main__':
    # Use the PORT environment variable provided by Heroku
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
