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
import random
import math
from collections import Counter
import traceback
import numpy as np
from scipy.stats import skew, kurtosis

# TODO: this probably won't work with an encrypted string unless there is a restricted byte in said encryption
EOF_CHR = '\0'

def derive_key(password: str) -> bytes:
    hashed = hashlib.sha256(password.encode()).digest()
    return base64.urlsafe_b64encode(hashed)

def encrypt_data(data: str, password: str) -> bytes:
    key = derive_key(password)
    f = Fernet(key)
    return f.encrypt(data.encode()) 

def calc_byte_counts(data):
    counts = Counter(data)
    return dict(counts)

def calc_entropy(byte_counts, total_bytes):
    entropy = 0.0
    for count in byte_counts.values():
        p_x = count / total_bytes
        entropy -= p_x * math.log2(p_x)
    return entropy

def hide_data(fileData, textData: str, img_width: int, img_height: int, key=None) -> io.BytesIO:
    width = list(range(img_width))
    height = list(range(img_height))
    # If key is provided, shuffle pixel order
    if key != None:
        random.seed(key)
        random.shuffle(width)
        random.shuffle(height)
    # work though each pixel, and its data (int)
    for x in width:
        for y in height:
            pixelData = list(fileData[x,y])
            for z in range(len(pixelData)):
                # change the last bit in the pixel's data to the text's next bit
                pixelData[z] = int(bin(pixelData[z])[2:-1]+textData[0],2)
                fileData[x,y] = tuple(pixelData)
                # truncate the data by that one bit
                textData = textData[1:]
                if(textData == ""):
                    return

def find_data(fileData, img_width: int, img_height: int, key=None) -> bytes:
    width = list(range(img_width))
    height = list(range(img_height))
    # If key is provided, shuffle pixel order
    if key != None:
        random.seed(key)
        random.shuffle(width)
        random.shuffle(height)
    textData = ""
    byteData = ""
    # work though each pixel
    for x in width:
        for y in height:
            for z in range(len(fileData[x,y])):
                # append the LSB of each pixel's data
                byteData += bin(fileData[x,y][z])[-1]
                if (len(byteData) == 8):
                    # once there is 8 bits, save it as a character
                    textData += chr(int(byteData,2))
                    # if that character is the EOF character, return
                    if (textData[-1]==EOF_CHR):
                        return textData[:-1]
                    byteData = ""
    return textData.encode('utf-8')

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

            # Open the image and make sure it is large enough to hide it
            img = Image.open(file.stream)
            if (len(data) > img.width * img.height * len(img.getbands()) // 8):
                # TODO Is returning an error the correct thing to do here?
                return jsonify({"successful": False, "message": "Image too small for provided password."}), 400

            # Add EOF Character to data, and convert data into a binary string
            if (EOF_CHR in data):
                # TODO, idk what to do here, return with an error?
                return jsonify({"successful": False, "message": "Invalid byte in data field"}), 400
            data += EOF_CHR
            dataString = ''.join(format(ord(byte), 'b').zfill(8) for byte in data)

            # Hide the data into the image, and save it to the output buffer
            hide_data(img.load(), dataString, img.width, img.height, key) #CHANGE:added key for shuffling
            output_buffer = io.BytesIO()
            img.save(output_buffer, "PNG")

            # reset buffer location before returning file
            output_buffer.seek(0) 
            return send_file(output_buffer, mimetype='image/png', as_attachment=True, download_name='encoded.png')

        except Exception as e:
            traceback.print_exc()
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
            # Make sure it is in PNG Format, may change this later
            if img.format != 'PNG':
                return jsonify({"successful": False, "message": "PNG format expected."}), 400

            print('test2')
            
            dataString = find_data(img.load(), img.width, img.height, key) #CHANGE:added key for shuffling

            return jsonify({"successful": True, "message": dataString})

        except Exception as e:
            traceback.print_exc()
            return jsonify({"successful": False, "message": str(e)}), 500

    # Analyze route
    @app.route('/analyze/', methods=['POST'])
    def analyze():
        try:
            file = request.files.get('file')

            # Testing
            img = Image.open(file.stream).convert('RGB')
            width, height = img.size
            mode = img.mode
            channels = len(mode)  # use the length of the string lol
            uncompressed_size = width * height * channels  # in bytes
            print(f"Uncompressed size: {uncompressed_size / (1024 * 1024):.2f} MB")
            print(img.mode)

            # Load and convert image to RGB
            img = Image.open(file.stream).convert('RGB')
            img_np = np.array(img)
            flat_bytes = img_np.flatten().astype(np.uint8)

            # Byte frequency
            byte_counts = Counter(flat_bytes)
            total_bytes = len(flat_bytes)
            entropy = -sum((count / total_bytes) * math.log2(count / total_bytes) for count in byte_counts.values())
            byte_counts_json = {int(k): int(v) for k, v in byte_counts.items()}

            # LSB uiformity
            lsb_array = flat_bytes & 1
            lsb_uniformity = float(np.std(lsb_array))

            # Byte statistics
            overall_stats = {
                'entropy': entropy,
                'lsb_uniformity': lsb_uniformity,
                'mean': float(np.mean(flat_bytes)),
                'median': float(np.median(flat_bytes)),
                'mode': int(np.bincount(flat_bytes).argmax()),
                'std_dev': float(np.std(flat_bytes)),
                'skewness': float(skew(flat_bytes)),
                'kurtosis': float(kurtosis(flat_bytes)),
            }

            # RGB statistics
            rgb_stats = {}
            for idx, channel in enumerate(['R', 'G', 'B']):
                values = img_np[:, :, idx].flatten()
                rgb_stats[channel] = {
                    'mean': float(np.mean(values)),
                    'median': float(np.median(values)),
                    'mode': int(np.bincount(values).argmax()),
                    'std_dev': float(np.std(values)),
                    'skewness': float(skew(values)),
                    'kurtosis': float(kurtosis(values)),
                }

            # Histograms per color
            histograms = {}
            for index, channel in enumerate(['R', 'G', 'B']):
                hist, _ = np.histogram(img_np[:, :, index], bins=256, range=(0, 256))
                histograms[channel] = {int(i): int(v) for i, v in enumerate(hist)}

            return jsonify({
                'overall_byte_stats': overall_stats,
                'rgb_stats': rgb_stats,
                'byte_counts': byte_counts_json,
                'histograms': histograms
            })

        except Exception as e:
            traceback.print_exc()
            return jsonify({"error": str(e)}), 500



    # run the app
    app.run(host='0.0.0.0', port=5000)


if __name__ == '__main__':
    main()
