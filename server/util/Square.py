"""Square.py
"""
class Square:
    """Superclass to model a single square on the game board.

    Attributes:
        id (int): Unique identifier for the Square.
        players (list[str]): List of players occupying the Square. 
        neighbors (list[Square]): List of adjacent Squares.

    """
    def __init__(self, id:str, players:list=[], neighbors:list=[]):
        self.id = id
        self.players = players
        self.neighbors = neighbors

    def setId(self, id:int):
        self.id = id

    def getId(self)->int:
        return self.id

    def setPlayers(self, players:list):
        self.players = players

    def getPlayers(self)->list:
        return self.players
    
    def setNeighbors(self, neighbors:list):
        self.neighbors = neighbors

    def getNeighbors(self)->list:
        return self.neighbors

    def addPlayer(self, name:str):
        """Function to add player to square.

        @param name (str): name of player

        """
        if len(self.players) < 4:
            self.players.append(name)
        else:
            raise ValueError("More than 4 players cannot occupy this square!")

    def removePlayer(self, name):
        """Function to remove player from square.

        @param name (str): name of player

        """
        if name in self.players:
            self.players.remove(name)
        else:
            raise ValueError(f"Player {name} is not occupying this square!")

    def addNeighbor(self, id:str):
        """Function to add neighbor to square.

        @param id (str): neighbor ID

        """
        if id not in self.neighbors:
            self.neighbors.append(id)
        else:
            raise ValueError(f"Square {id} is already a neighbor!")

    def removeNeighbor(self, id:str):
        """Function to remove neighbor from square.

        @param id (str): neighbor ID

        """
        if id in self.neighbors:
            self.neighbors.remove(id)
        else:
            raise ValueError(f"Square {id} is not already a neighbor!")

class CategorySquare(Square):
    """Subclass to model square with a category.

    Attributes:
        color (str): Color associated with the Square.
        isHQ (bool): True if square is an HQ Square.

    """
    def __init__(self, id:str, players:list, neighbors:list, color:str, isHQ:bool=False):
        super().__init__(id, players, neighbors)
        self.color = color
        self.isHQ = isHQ

    def setColor(self, color:str):
        self.color = color

    def getColor(self)->str:
        return self.color

    def setIsHQ(self, isHQ:bool):
        self.isHQ = isHQ

    def getIsHQ(self)->str:
        return self.isHQ

class RollAgainSquare(Square):
    """Subclass to model the corner Roll Again Squares.

    """
    def __init__(self, id:str, players:list, neighbors:list):
        super().__init__(id, players, neighbors)

class CenterSquare(Square):
    """Subclass to model the board's neutral center square.

    """
    def __init__(self, id:str, players:list, neighbors:list):
        super().__init__(id, players, neighbors)

