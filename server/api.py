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

# TODO: this probably won't work with an encrypted string unless there is a restricted byte in said encryption
EOFCHAR = '\r'

def derive_key(password: str) -> bytes:
    hashed = hashlib.sha256(password.encode()).digest()
    return base64.urlsafe_b64encode(hashed)

def encrypt_data(data: str, password: str) -> bytes:
    key = derive_key(password)
    f = Fernet(key)
    return f.encrypt(data.encode()) 

def hide_data(fileData, textData: str, width: int, height: int) -> io.BytesIO:
    # work though each pixel, and its data (int)
    for x in range(width):
        for y in range(height):
            pixelData = list(fileData[x,y])
            for z in range(len(pixelData)):
                # change the last bit in the pixel's data to the text's next bit
                pixelData[z] = int(bin(pixelData[z])[2:-1]+textData[0],2)
                fileData[x,y] = tuple(pixelData)
                # truncate the data by that one bit
                textData = textData[1:]
                if(textData == ""):
                    return

def find_data(fileData, width: int, height: int) -> bytes:
    textData = ""
    byteData = ""
    # work though each pixel
    for x in range(width):
        for y in range(height):
            for z in range(len(fileData[x,y])):
                # append the LSB of each pixel's data
                byteData += bin(fileData[x,y][z])[-1]
                if (len(byteData) == 8):
                    # once there is 8 bits, save it as a character
                    textData += chr(int(byteData,2))
                    # if that character is the EOF character, return
                    if (textData[-1]==EOFCHAR):
                        return textData[:-1].encode('utf-8')
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

            # Open image and convert to png
            img = Image.open(file.stream)
            output_buffer = io.BytesIO()
            img.save(output_buffer, "png")

            # Encrypt data and make sure the image is large enough to hide it
            # TODO make sure the encrypt function works
            data = encrypt_data(data, key)     
            if (len(data) > img.width * img.height * len(img.getbands()) // 8):
                # TODO Is returning an error the correct thing to do here?
                return jsonify({"successful": False, "message": "Image too small for provided password."}), 400

            # Add EOF Character to data, and convert data into a binary string
            data += EOFCHAR.encode('utf-8')
            dataString = ''.join(f'{byte:08b}' for byte in data)

            # Hide the data into the image, and save it to the output buffer
            hide_data(img.load(), dataString, img.width, img.height)
            img.save(output_buffer, "png")

            output_buffer.seek(0) # reset buffer location before returning file
            return send_file(output_buffer, mimetype='image/png', as_attachment=True, download_name='encoded.png')

        except Exception as e:
            return jsonify({"successful": False, "message": str(e)}), 500


    # Decode route
    @app.route('/decode/', methods=['POST'])
    def decode():
        try:
            file = request.files.get('file')
            key = request.form.get('key')

            print('test1')
            if not file or not key:
                return jsonify({"successful": False, "message": "Missing required data."}), 400

            img = Image.open(file.stream)
            # Make sure it is in PNG Format, may change this later
            if img.format != 'PNG':
                return jsonify({"successful": False, "message": "PNG format expected."}), 400

            print('test2')
            data = find_data(img.load(), img.width, img.height)

            # TODO decrypt the data
            dataString = data.decode('utf-8')

            print('test3')
            return jsonify({"successful": True, "message": dataString})

        except Exception as e:
            return jsonify({"successful": False, "message": str(e)}), 500


    # run the app
    app.run(host='0.0.0.0', port=5000)


if __name__ == '__main__':
    main()
