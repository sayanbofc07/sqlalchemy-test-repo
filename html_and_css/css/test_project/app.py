from flask import Flask, render_template, request
from flask_cors import CORS
import os,time

app = Flask(__name__)
CORS(app)

UPLOAD_FOLDER = 'uploads'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    uploaded_file = request.files.get('file')
    if uploaded_file:
        file_path = os.path.join(UPLOAD_FOLDER, uploaded_file.filename)
        time.sleep(10)
        uploaded_file.save(file_path)
        return 'File uploaded successfully', 200
    return 'No file uploaded', 400

if __name__ == '__main__':
    app.run(debug=True)
