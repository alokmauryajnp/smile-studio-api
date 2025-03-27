from flask import Flask, request, jsonify
import cv2
import numpy as np
from deepface import DeepFace
import os

app = Flask(__name__)

UPLOAD_FOLDER = "uploads"
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

def enhance_teeth(image_path):
    img = cv2.imread(image_path)
    # Simple whitening effect
    img = cv2.addWeighted(img, 1.5, np.zeros(img.shape, img.dtype), 0, -30)
    enhanced_path = os.path.join(UPLOAD_FOLDER, "enhanced_teeth.jpg")
    cv2.imwrite(enhanced_path, img)
    return enhanced_path

@app.route("/process", methods=["POST"])
def process_image():
    if "image" not in request.files:
        return jsonify({"error": "No image uploaded"}), 400

    file = request.files["image"]
    image_path = os.path.join(UPLOAD_FOLDER, "input.jpg")
    file.save(image_path)

    enhanced_path = enhance_teeth(image_path)
    return jsonify({"enhanced_image": enhanced_path})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
