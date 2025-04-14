from flask import Flask, jsonify, request, send_file
from flask_cors import CORS
from util.User import User
from util.GameUtils import GameUtils
from util.GameSession import GameSession
from util.Gameboard import Gameboard
from util.Question import Question, Board
from util.Database import Database
from werkzeug.utils import secure_filename
from util.MultimediaUtils import convert_to_blob, convert_to_file, clear_old_multimedia
from PIL import Image
import io
from cryptography.fernet import Fernet
import base64
import hashlib
import os

def derive_key(password: str) -> bytes:
    hashed = hashlib.sha256(password.encode()).digest()
    return base64.urlsafe_b64encode(hashed)

def encrypt_data(data: str, password: str) -> bytes:
    key = derive_key(password)
    f = Fernet(key)
    return f.encrypt(data.encode()) 

def main():
    # start new flask app
    app = Flask(__name__)
    CORS(app)
    
    path = os.path.dirname(os.path.abspath(__file__))
    uploads_path = path.replace("server", "client")
    uploads_path = os.path.join(uploads_path, "public")
    

    # Test route
    @app.route('/test', methods=['GET'])
    def home_page():
        print('test route')
        return jsonify("test route")
    
    # Encode route
    @app.route('/encode/', methods=['POST'])
    def encode():
        try:
            file = request.files.get('file')
            key = request.form.get('key')
            data = request.form.get('data')
            
            if not file or not key or not data:
                return jsonify({"successful": False, "message": "Missing required data."}), 400

            img = Image.open(file.stream)

            output_buffer = io.BytesIO()
            img.save(output_buffer, format="PNG")  # TODO add file type check for JPEG or PNG
            output_buffer.seek(0)

            return send_file(output_buffer, mimetype='image/png', as_attachment=True, download_name='encoded.png')

        except Exception as e:
            return jsonify({"successful": False, "message": str(e)}), 500


    # Decode route
    @app.route('/decode/', methods=['POST'])
    def decode():
        try:
            file = request.files.get('file')
            key = request.form.get('key')

            if not file or not key:
                return jsonify({"successful": False, "message": "Missing required data."}), 400

            img = Image.open(file.stream)

            output_buffer = io.BytesIO()
            img.save(output_buffer, format="PNG")  # TODO add file type check for JPEG or PNG
            output_buffer.seek(0)

            data = "this is data"

            return jsonify({"successful": True, "message": data})

        except Exception as e:
            return jsonify({"successful": False, "message": str(e)}), 500


    # run the app
    app.run(host='0.0.0.0', port=5000)


if __name__ == '__main__':
    main()
