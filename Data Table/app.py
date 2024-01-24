from flask import Flask, request, jsonify
import pandas as pd
import os

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'

# Ensure the upload folder exists
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

@app.route('/upload', methods=['POST', 'GET'])
def upload_file():
    # Check if a file is part of the request
    if 'fileUpload' not in request.files:
        return jsonify({'error': 'No file part'})

    file = request.files['fileUpload']

    # If the user does not select a file, the browser submits an empty file without a filename
    if file.filename == '':
        return jsonify({'error': 'No selected file'})

    if file and file.filename.endswith(('.xlsx', '.xls')):
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        file.save(file_path)
        df = pd.read_excel(file_path)

        # Assuming the Excel file has columns 'Name', 'Firm', 'Email', and 'Role'
        names = df['Name'].tolist()
        firms = df['Firm'].tolist()
        emails = df['Email'].tolist()
        roles = df['Role'].tolist()

        # Process the data as needed
        # ...

        return jsonify({'message': 'File successfully uploaded and processed'})
    else:
        return jsonify({'error': 'No Excel file uploaded or wrong file format'})

if __name__ == '__main__':
    app.run(debug=True, port=5000)
