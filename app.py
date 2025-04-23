from flask import Flask, render_template, request, Response
import json
import csv
import io

app = Flask(__name__)

def json_to_csv(json_data):
    if isinstance(json_data, dict):
        json_data = [json_data]

    if not json_data:
        return ""

    output = io.StringIO()
    writer = csv.DictWriter(output, fieldnames=json_data[0].keys())
    writer.writeheader()
    for row in json_data:
        writer.writerow(row)
    
    return output.getvalue()

@app.route('/', methods=['GET', 'POST'])  # ✅ This line is key
def upload_file():
    if request.method == 'POST':
        file = request.files['file']
        if file and file.filename.endswith('.json'):
            try:
                json_data = json.load(file)
                csv_data = json_to_csv(json_data)
                return Response(
                    csv_data,
                    mimetype='text/csv',
                    headers={"Content-Disposition": "attachment;filename=converted.csv"}
                )
            except Exception as e:
                return f"Error processing file: {e}"
        else:
            return "Please upload a valid .json file"
    
    return render_template("index.html")
