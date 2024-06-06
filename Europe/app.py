<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Upload Photos</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            margin: 0;
            padding: 0;
            background-color: #f2f2f2; /* Light gray background */
        }

        .container {
            max-width: 400px; /* Centered container with maximum width */
            margin: 50px auto; /* Center the container vertically and horizontally */
            padding: 20px;
            background-color: #fff; /* White background */
            border-radius: 8px;
            box-shadow: 0 0 10px rgba(0, 0, 0, 0.1); /* Subtle shadow for depth */
        }

        h1 {
            text-align: center;
            margin-bottom: 20px; /* Add spacing below the heading */
        }

        form {
            text-align: center;
        }

        input[type="file"] {
            display: block;
            margin: 20px auto; /* Center the file input */
        }

        #coordinates {
            margin-top: 20px; /* Add spacing above the coordinates section */
            padding: 10px;
            border: 1px solid #ccc;
            border-radius: 5px;
            text-align: center; /* Center the text */
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>Upload Photos</h1>
        <form id="upload-form" enctype="multipart/form-data" action="/upload" method="post">
            <input type="file" name="photo" id="photo-input" accept="image/*" multiple>
            <input type="submit" id="upload-btn" value="Upload">
        </form>
        <div id="coordinates" style="display:none;">
            <h2>GPS Coordinates:</h2>
            <p id="latitude"></p>
            <p id="longitude"></p>
        </div>
    </div>

    <script src="https://code.jquery.com/jquery-3.6.0.min.js"></script>
    <script>
        $(document).ready(function() {
            $('#upload-form').submit(function(event) {
                // Prevent form submission
                event.preventDefault();
                // Perform AJAX request to upload the file
                $.ajax({
                    url: '/upload',
                    type: 'POST',
                    data: new FormData(this),
                    processData: false,
                    contentType: false,
                    dataType: 'json', // Expect JSON response
                    success: function(response) {
                        // Show the hidden coordinates div
                        $('#coordinates').show();
                        // Parse and display the GPS coordinates
                        $('#latitude').text('Latitude: ' + response.latitude);
                        $('#longitude').text('Longitude: ' + response.longitude);
                    },
                    error: function(xhr, status, error) {
                        // Display error message if any
                        alert('Error: ' + error);
                    }
                });
            });
        });
    </script>
</body>
</html>
