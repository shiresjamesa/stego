"""GameSession.py
"""
from util.GameUtils import GameUtils
from util.Player import Player

class GameSession:
    """Class to simulate the game session. 

    Attributes:
        players (list[Player]): List of Players
        categories (list[str]): List of categories
        gameboard (Gameboard): Gameboard object

    Methods:
        initializePlayers:
        initializeGame:
        query: 
        filter: 
        first: 
        exists:
        commit:
        close:
    """
    # list of HQ square IDs
    HQ_LIST = ["A4", "E0", "E8", "I4"]

    # list of Roll Again square IDs
    ROLL_AGAIN_LIST = ["A0", "A8", "I0", "I8"]

    HOME_SQUARE = "E4"

    def __init__(self, names:list, categories:list, gameboard):
        self.gameboard = gameboard
        self.categories = []
        for category in categories:
            cat = category.replace(" ", "")
            self.categories.append(cat)
        self.curPlayerI = 0

        self.initializePlayers(names)
        self.initializeGame()

    def setPlayers(self, players:list):
        self.players = players

    def getPlayers(self)->list:
        return self.players

    def setCategories(self, categories:list):
        self.categories = categories

    def getCategories(self)->list:
        return self.categories

    def setGameboard(self, gameboard):
        self.gameboard = gameboard

    def getGameboard(self):
        return self.gameboard

    def getCurrentPlayer(self):
        """Function to return player who is currently taking turn
        """
        return self.players[self.curPlayerI]

    def updatePlayerLoc(self, move):
        self.players[self.curPlayerI].setLocation(move)

    def initializePlayers(self, names):
        """Function to initialize players from list of names.

        @param names (list): list of player names

        """
        # initialize wedge dictionary
        wedges = {}
        for category in self.categories:
            wedges[category] = False

        # build player objects
        players = []
        for i, name in enumerate(names):
            player = Player(name = name, wedges = wedges)
            players.append(player)

        self.players = players

    def initializeGame(self):
        """Function to initialize game session
        """
        # add players to center square
        for player in self.players:
            self.gameboard.squares["E4"].addPlayer(player.getName())

    def handleAnswer(self, isCorrect, category):
        """Function to process answer status
        """
        isWinner = False

        # remove whitespace from category name
        category = category.replace(" ", "")

        curPlayer = self.getCurrentPlayer()

        curPlayerLoc = curPlayer.getLocation()

        # check if player on Roll Again square
        if curPlayerLoc in self.ROLL_AGAIN_LIST:
            return (self.curPlayerI + 1, isWinner)

        if isCorrect:
            # check if player on an HQ square
            if curPlayerLoc in self.HQ_LIST:
                self.players[self.curPlayerI].addWedge(category)
            elif curPlayerLoc == self.HOME_SQUARE:
                if curPlayer.wedgesComplete():
                    isWinner = True

        else:
            # if incorrect, next player's turn
            self.curPlayerI = (self.curPlayerI + 1) % len(self.players)
            curPlayer = self.players[self.curPlayerI]
            
        return (self.curPlayerI + 1, isWinner)

        
        

