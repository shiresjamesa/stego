"""Player.py
"""
class Player:
    """Class to model a Trival Compute Player.

    Attributes:
        name (str): Name of Player
        isTurn (bool): Indicates if it is currently Player's turn
        color (str): Color of Player's token
        wedges (dict): Dictionary of booleans indicating earned wedges
        location (str): Current location of Player on the gameboard

    Methods:
        move:
        answer_question:
        update_score:
    """
    def __init__(self, name:str, wedges:dict={}, location:str="E4"):
        self.name = name
        self.wedges = wedges
        self.location = location

    def setName(self, name:str):
        self.name = name

    def getName(self)->str:
        return self.name

    def setWedges(self, wedges:dict):
        self.wedges = wedges

    def getWedges(self)->dict:
        return self.wedges

    def setLocation(self, location:str):
        self.location = location

    def getLocation(self)->str:
        return self.location

    def addWedge(self, category:str):
        """Function to add wedge to player's score.

        @param category (str): category of wedge

        """
        if category in self.wedges:
            self.wedges[category] = True

    def wedgesComplete(self):
        """Function to check if player has all wedges
        
        @ retruns bool: boolean indicating if player has all wedges or not

        """
        for category in self.wedges:
            if not self.wedges[category]:
                return False
        return True

