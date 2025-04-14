import os

def convert_to_blob(filename):
    with open(filename, "rb") as open_file:
        blob = open_file.read()

    return blob

def convert_to_file(filename:str, blob:bytes):
    with open(filename, "wb") as open_file:
        open_file.write(blob)

    return filename

def clear_old_multimedia(filepath:str):

    # assert that we are in the right filepath
    assert filepath[-6:].endswith("public")

    files = []

    # do it like this so we don't get errors for some reason
    for file in os.listdir(filepath):
        files.append(os.path.join(filepath, file))

    for filepath in files:
        os.remove(filepath)
        