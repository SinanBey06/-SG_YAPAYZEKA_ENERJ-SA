from flask import Flask, request, jsonify, send_from_directory, render_template
from werkzeug.utils import secure_filename
from flask_cors import CORS
import os
import time
from pymongo import MongoClient


app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Configure upload folder and allowed extensions
app.config['UPLOAD_FOLDER'] = 'uploads/'
app.config['ALLOWED_EXTENSIONS'] = {'mp4', 'avi', 'mov'}

# MongoDB connection
client = MongoClient('mongodb://localhost:27017/')
db = client['enerjisa']  
collection = db['enerjisa_ai2'] 
video_id = ""

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    global video_id
    
    if 'file' not in request.files:
        return jsonify({'error': 'No file part in the request'}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400

    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(file_path)

        # Simulating video processing delay
        time.sleep(2)  # Simulate 2 seconds delay

        # Save to MongoDB
        uploaded_url = f"/uploads/{filename}"
        
        
        
        # Save data to MongoDB
        upload_data = {
            'filename': filename,
            'file_path': uploaded_url,
            'selected_items': [],
            'analysis_result': [],
            'upload_time': time.time(),
            "analysis_time": 0
        }
        video_id = collection.insert_one(upload_data).inserted_id

        # Prepare response
        video_info = {
            'filename': filename,
            'size': os.path.getsize(file_path) / (1024 * 1024),  # Size in MB
            'resolution': "Replace with actual resolution"
        }
        return jsonify({'video_info': video_info, 'video_path': uploaded_url}), 200

    else:
        return jsonify({'error': 'File not allowed'}), 400



@app.route('/analysis', methods=['POST'])
def analysis_items_endpoint():
    selected_items = request.json.get('selectedItems')  # Analiz için seçilen itemler
        
    # AI çıktısı
    # AI çıktısı
    # AI çıktısı
    # AI çıktısı
    # AI çıktısı
    # AI çıktısı
    analysis_result = ["Gözlük", "Eldiven"]   # modelin çıktısı
    
    collection.update_one({"_id": video_id}, 
        {"$set": {"selected_items": selected_items, "analysis_result": analysis_result, "analysis_time": time.time()}})
    
    
    return jsonify({'analysis_result': analysis_result}), 200






@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)


if __name__ == '__main__':
    if not os.path.exists(app.config['UPLOAD_FOLDER']):
        os.makedirs(app.config['UPLOAD_FOLDER'])
    app.run(debug=True)
