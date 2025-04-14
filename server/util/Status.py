"""Status.py
"""

class Status():
    '''
    aux class to send messages from server to front end

    Attributes:
        boolean (bool): operation successful
        message (str): status message
    '''

    def __init__(self, boolean: bool, message: str) -> None:
        self.boolean = boolean
        self.message = message

    def __repr__(self):
        return f"Operation successful: {self.boolean} | Status message: {self.message}"