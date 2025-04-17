# from flask import Flask, render_template, request, send_file
# import os
# import json
# import csv
# from werkzeug.utils import secure_filename

# app = Flask(__name__)

# UPLOAD_FOLDER = 'uploads'
# OUTPUT_FOLDER = 'output'

# # Create folders only if they don’t exist
# if not os.path.exists(UPLOAD_FOLDER):
#     os.makedirs(UPLOAD_FOLDER)

# if not os.path.exists(OUTPUT_FOLDER):
#     os.makedirs(OUTPUT_FOLDER)

# @app.route('/')
# def index():
#     return render_template('index.html')

# @app.route('/convert', methods=['POST'])
# def convert():
#     if 'json_file' not in request.files:
#         return 'No file part', 400

#     file = request.files['json_file']
#     if file.filename == '':
#         return 'No selected file', 400

#     if file:
#         filename = secure_filename(file.filename)
#         filepath = os.path.join(UPLOAD_FOLDER, filename)
#         file.save(filepath)

#         with open(filepath, 'r') as f:
#             try:
#                 data = json.load(f)
#             except json.JSONDecodeError:
#                 return 'Invalid JSON file', 400

#         # Normalize if the root is a dictionary
#         if isinstance(data, dict):
#             data = [data]

#         if not isinstance(data, list):
#             return 'JSON must be an object or list of objects', 400

#         if len(data) == 0:
#             return 'Empty JSON file', 400

#         # Create CSV
#         csv_filename = filename.rsplit('.', 1)[0] + '.csv'
#         csv_path = os.path.join(OUTPUT_FOLDER, csv_filename)

#         with open(csv_path, 'w', newline='') as csvfile:
#             writer = csv.DictWriter(csvfile, fieldnames=data[0].keys())
#             writer.writeheader()
#             for item in data:
#                 writer.writerow(item)

#         return send_file(csv_path, as_attachment=True)

#     return 'File upload failed', 500

# if __name__ == '__main__':
#     app.run(debug=True)


from flask import Flask, render_template, request, send_file
import os
import json
import csv
from werkzeug.utils import secure_filename

app = Flask(__name__)

UPLOAD_FOLDER = 'uploads'
OUTPUT_FOLDER = 'output'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['OUTPUT_FOLDER'] = OUTPUT_FOLDER

os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        file = request.files['json_file']
        if file and file.filename.endswith('.json'):
            filename = secure_filename(file.filename)
            json_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(json_path)

            # Convert JSON to CSV
            with open(json_path, 'r') as f:
                data = json.load(f)

            # Handle if JSON is not a list
            if isinstance(data, dict):
                data = [data]

            csv_filename = filename.rsplit('.', 1)[0] + '.csv'
            csv_path = os.path.join(app.config['OUTPUT_FOLDER'], csv_filename)

            with open(csv_path, 'w', newline='') as csvfile:
                writer = csv.DictWriter(csvfile, fieldnames=data[0].keys())
                writer.writeheader()
                writer.writerows(data)

            return send_file(csv_path, as_attachment=True)

    return render_template('index.html')
