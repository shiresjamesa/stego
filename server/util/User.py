"""User.py
"""
import hashlib

# User Class
class User():
    '''
    Class to represent a Trivial-Compute User

    Attributes:
        username (str): username of the user
        password (str): password of the user
        email (str): email of the user
    '''
    
    # Initialize Schema
    def __init__(self, id:str, username: str, password: str, email: str):
        self.id = id
        self.username = username
        self.password = str(hashlib.sha256(bytes(password, "utf-8")).hexdigest())
        self.email = email
    
    # Printing Schema
    def __repr__(self):
        return f"Username: {self.username}"
