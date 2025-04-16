from PIL import Image
import io
import random

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
                    if (textData[-1]==EOFCHAR):
                        return textData[:-1]#.encode('utf-8') #CHANGE
                    byteData = ""
    return textData.encode('utf-8')

file1="tests/example.jpg"
file2="tests/outputR.png"
key="password"
data="hello world"
EOFCHAR = "\r"
MODE = "D"

img = Image.open(file1)
output_buffer = io.BytesIO()
img.save(output_buffer, "PNG")

if MODE == "E":
    if (len(data) > img.width * img.height * len(img.getbands()) // 8):
        print("Image too small")
        exit()
    data += EOFCHAR
    dataString = ''.join(format(ord(byte), 'b').zfill(8) for byte in data)
    hide_data(img.load(), dataString, img.width, img.height, key) #CHANGE:added key
    img.save(output_buffer, "png")

    img.save(file2, "PNG")

if MODE == "D":
    img = Image.open(file2)
    # Make sure it is in PNG Format, may change this later
    if img.format != 'PNG':
        print("PNG format expected.")
        exit()
        
    data = find_data(img.load(), img.width, img.height, key) #CHANGE:added key

    print(data)
