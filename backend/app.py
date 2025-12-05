from flask import Flask, request, jsonify
from flask_cors import CORS
import os

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})

if not os.path.exists("uploads"):
    os.makedirs("uploads")

@app.route("/upload", methods=["POST"])
def upload():
    file = request.files.get("file")
    if not file:
        return jsonify({"error": "No file uploaded"}), 400

    filename = file.filename
    filepath = os.path.join("uploads", filename)
    file.save(filepath)
    return jsonify({"message": f"Received {filename}"}), 200

if __name__ == "__main__":
    app.run(port=5000, debug=True)
