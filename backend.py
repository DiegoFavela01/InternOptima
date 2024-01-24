from flask import Flask, request, jsonify, render_template
import random
import pandas as pd
import os

app = Flask(__name__)

UPLOAD_FOLDER = 'uploads'

# Ensure uploads directory exists
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)


@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

@app.route('/generate_email', methods=['POST'])
def generate_email():
    try:
        # Handle text fields
        data = request.form.to_dict(flat=False)
        username = data['Username'][0]
        major = data['Major'][0]
        university = data['University'][0]

        # Handle Excel file upload
        file = request.files['fileUpload']
        if file and file.filename.endswith(('.xlsx', '.xls')):
            file_path = os.path.join('uploads', file.filename)
            file.save(file_path)
            df = pd.read_excel(file_path)

            # Assuming the Excel file has columns 'Name', 'Firm','Email' and "Role"
            names = df['Name'].tolist()
            firms = df['Firm'].tolist()
            emails = df['Email'].tolist()
            roles = df['Role'].tolist()
        else:
            return jsonify({'error': 'No Excel file uploaded or wrong file format'})

        generated_emails = []
        for name, firm, email, role in zip(names, firms, emails, roles):
            with open('email_templates.txt', 'r', encoding='utf-8') as file:
                email_templates = file.read().split('---')
            email_template = random.choice(email_templates).strip()

            generated_email = email_template.format(
                Name=name, Firm=firm, Email=email, Role=role,
                Username=username, Major=major, University=university
            )
            generated_emails.append(generated_email)

        return jsonify({'emails': generated_emails})
    except Exception as e:
        return jsonify({'error': str(e)})

if __name__ == '__main__':
    app.run(debug=True, port=5001)
