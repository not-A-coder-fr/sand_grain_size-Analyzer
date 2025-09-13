from flask import Flask, Blueprint, render_template, jsonify, request, send_from_directory
import os
import time
from datetime import datetime
from .utils.camera import capture_image
from .utils.yolo_grain_detector import detect_grains
from .utils.tof_calibrate import get_distance
from .utils.gnss_parser import get_location
from .utils.image_processor import process_image_and_save_results
import config

bp = Blueprint('main', __name__)

def create_app():
    app = Flask(__name__, template_folder='templates')
    app.register_blueprint(bp)
    return app

@bp.route('/')
def index():
    return render_template('index.html')

@bp.route('/capture', methods=['POST'])
def capture():
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"IMG_{timestamp}.jpg"
    filepath = os.path.join(config.IMAGE_DIR, filename)

    # Save uploaded image
    image = request.files['image']
    image.save(filepath)
    
    # Get ToF distance
    tof_dist = get_distance()
    if tof_dist is None:
        return jsonify({"error": "ToF sensor failed"}), 500

    # Get GNSS location
    lat, lon = get_location()
    if lat is None or lon is None:
        return jsonify({"error": "GNSS failed"}), 500

    # Process image and save results
    result = process_image_and_save_results(filepath, tof_dist, lat, lon)

    return jsonify({
        "success": True,
        "image": filename,
        "result": result
    })

@bp.route('/results')
def results():
    if not os.path.exists(config.RESULT_FILE):
        return render_template('results.html', results=[], error="No results yet.")
    
    import csv
    results = []
    with open(config.RESULT_FILE, 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            results.append(row)
    
    latest = results[-1] if results else {}
    return render_template('results.html', results=[latest])

@bp.route('/images/<filename>')
def serve_image(filename):
    return send_from_directory(config.IMAGE_DIR, filename)