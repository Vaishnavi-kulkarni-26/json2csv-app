from flask import Flask, request, send_file, render_template
import os
import json
import csv
import uuid

app = Flask(__name__)

OUTPUT_FOLDER = 'output'

# Make sure 'output' folder exists and is a folder, not a file
if os.path.exists(OUTPUT_FOLDER) and not os.path.isdir(OUTPUT_FOLDER):
    os.remove(OUTPUT_FOLDER)

os.makedirs(OUTPUT_FOLDER, exist_ok=True)

@app.route('/')
def index():
    return render_template('index.html')  # your frontend page

@app.route('/convert', methods=['POST'])
def convert_json_to_csv():
    if 'file' not in request.files:
        return 'No file uploaded', 400

    file = request.files['file']
    if not file.filename.endswith('.json'):
        return 'File must be a JSON', 400

    try:
        json_data = json.load(file)
    except json.JSONDecodeError:
        return 'Invalid JSON file', 400

    if isinstance(json_data, dict):
        # wrap in a list to write rows
        json_data = [json_data]

    # Generate a unique output file name
    output_filename = f"{uuid.uuid4().hex}.csv"
    output_path = os.path.join(OUTPUT_FOLDER, output_filename)

    # Write CSV
    with open(output_path, 'w', newline='') as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=json_data[0].keys())
        writer.writeheader()
        writer.writerows(json_data)

    return send_file(output_path, as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)
