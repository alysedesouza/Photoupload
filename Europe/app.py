from flask import Flask, request, jsonify, render_template
from pyproj import Transformer
 
# # Define source and destination CRS codes
 
# zone = int(input("enter in the zone, 49-56 "))

# source_crs = 28300+zone
# destination_crs = 7800+zone

# # Create a Transformer object with the specified CRS
# transformer = Transformer.from_crs(source_crs, destination_crs)

# # Prompt the user to enter the eastings and northings
# eastings = float(input("Enter the eastings: "))
 
# northings = float(input("Enter the northings: "))

# Perform the transformation
# transformed_point = transformer.transform(eastings, northings)
 
# print("Transformed point:", transformed_point)

app = Flask(__name__)

@app.route('/')
def home():
    # Renders the index.html template
    return render_template('index.html')

@app.route('/convert_coordinates', methods=['POST'])
def convert_coordinates():
    data = request.json
    zone = int(data['zone'])
    eastings = float(data['eastings'])
    northings = float(data['northings'])

    source_crs = 28300 + zone
    destination_crs = 7800 + zone

    transformer = Transformer.from_crs(source_crs, destination_crs)
    transformed_point = transformer.transform(eastings, northings)

    return jsonify({
        'transformed_easting': transformed_point[0],
        'transformed_northing': transformed_point[1]
    })

if __name__ == '__main__':
    app.run(debug=True)
