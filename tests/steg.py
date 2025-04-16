## These will be changed based on web app input
FILENAME = "output.jpg"
NEW_FILE = "output1.jpg"
PASSWORD = "password"
PASSWORD2= "" # used for debugging
MODE = "DE"
if(MODE == "DE"):
    PASSWORD = ""
    FILENAME = NEW_FILE
##

from PIL import Image
class StopImage(Exception):
    pass

def ctoa(letter):
    a = bin(ord(letter))[2:]
    return a.zfill(8)

# Find out if the provided file is usable, if so get the max number of characters it can store
img = None
dat = None
#v2 TODO: If Pillow.verify() then load as a list, else read file as bytes
try:
    img = Image.open(FILENAME)
except (OSError) as e:
    print("File format not accepted: {e}")
    exit
if (img == None):
    print("Provided file is empty. Exiting...")
    exit
maxLen = img.width * img.height * len(img.getbands()) // 8
dat = img.load()

# START OF ENCRYPTION/DECRYPTION #

if MODE == "EN" or MODE == "debug":
    if len(PASSWORD) > maxLen:
        print("password is too long for this image")
        PASSWORD = PASSWORD[0:maxLen]
        print("shortening to ",PASSWORD)
    else:
        PASSWORD += "\r"
    # TODO: Encrypt password here?

#v2 TODO: put this all in a function and return on finish rather than raise
extract = ""
extract2= "" # Used for debugging
try:
    for x in range(img.width):
        for y in range(img.height):
            for z in range(len(dat[x,y])): #or len(img.getbands())
                if(MODE == "EN" or MODE == "debug"):
                    # load up extract with ascii bin of the next chr
                    if (extract == ""):
                        extract = ctoa(PASSWORD[0])
                        PASSWORD = PASSWORD[1:]
                    # change the LSB of z's value to the next bit
                    a = list(dat[x,y]) #TODO Not needed if loaded correctly
                    a[z] = int(bin(dat[x,y][z])[2:-1]+extract[0],2)
                    dat[x,y] = tuple(a)
                    extract = extract[1:]
                    # if both extract and password are empty, stop
                    if (extract == "" and PASSWORD == ""):
                        ## DONE ENCRYPTING ##
                        raise StopImage
                if (MODE == "DE" or MODE == "debug"):
                    # get the LSB of z's value
                    extract2 += bin(dat[x,y][z])[-1]
                    # when you have 8 bits, get the ascii chr
                    if (len(extract2) == 8):
                        PASSWORD2 += chr(int(extract2,2))
                        if (PASSWORD2[-1]=='\r'):
                            ## DONE DECRYPTING ##
                            raise StopImage
                        extract2 = ""
except StopImage:
    if(MODE == "DE"):
        print(PASSWORD[:-1])
    if(MODE == "EN"):
        ## TODO convert list back into tuples
        img.save(NEW_FILE)