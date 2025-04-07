from flask import Flask, render_template, request, jsonify
import os
import cv2
import numpy as np

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'static/images'

# Ensure the upload folder exists
if not os.path.exists(app.config['UPLOAD_FOLDER']):
    os.makedirs(app.config['UPLOAD_FOLDER'])

# Simple dehazing function (replace with a proper ML model if needed)
def dehaze_image(image_path):
    # Load the image
    image = cv2.imread(image_path)
    
    # Apply a simple dehazing technique (e.g., CLAHE for contrast enhancement)
    lab = cv2.cvtColor(image, cv2.COLOR_BGR2LAB)
    l, a, b = cv2.split(lab)
    clahe = cv2.createCLAHE(clipLimit=3.0, tileGridSize=(8, 8))
    l = clahe.apply(l)
    lab = cv2.merge((l, a, b))
    dehazed_image = cv2.cvtColor(lab, cv2.COLOR_LAB2BGR)
    
    # Save the dehazed image
    dehazed_image_path = os.path.join(app.config['UPLOAD_FOLDER'], 'dehazed_' + os.path.basename(image_path))
    cv2.imwrite(dehazed_image_path, dehazed_image)
    
    return dehazed_image_path

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/dehaze', methods=['POST'])
def dehaze():
    if 'image' not in request.files:
        return jsonify({'error': 'No image uploaded'}), 400
    
    file = request.files['image']
    if file.filename == '':
        return jsonify({'error': 'No image selected'}), 400
    
    # Save the uploaded image
    original_image_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
    file.save(original_image_path)
    
    # Dehaze the image
    dehazed_image_path = dehaze_image(original_image_path)
    
    # Return the paths of the original and dehazed images
    return jsonify({
        'original_image': original_image_path,
        'dehazed_image': dehazed_image_path
    })

if __name__ == '__main__':
    app.run(debug=True)