from flask import Flask, request,send_from_directory,render_template,Response
from ultralytics import YOLO
from flask import Flask, jsonify
from utils import image_detect, video_detect


app = Flask(__name__)
RESULT_FOLDER= r'static/results'
UPLOAD_FOLDER = 'static/uploads'
app.config['RESULT_FOLDER'] = RESULT_FOLDER
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
model = YOLO(r'models/best.pt')

@app.route('/')
def index():
    return render_template(r'index.html')

@app.route('/detect-image', methods=['POST'])
def detect_image():
    file = request.files.get('image')
    output_filename = image_detect(file, app.config['UPLOAD_FOLDER'], app.config['RESULT_FOLDER'], model)
    
    return jsonify({'result': f'/static/results/{output_filename}'})

@app.route('/detect-video', methods=['POST'])
def detect_video():
    file = request.files['video']
    video_url = video_detect(file, app.config['UPLOAD_FOLDER'], app.config['RESULT_FOLDER'], model)
    
    return jsonify({"result": video_url}), 200



if __name__ == '__main__':
    try:
        app.run(debug=True, host='0.0.0.0', port=5000)
    finally:
        print("Server stopped.")