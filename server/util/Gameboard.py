"""Gameboard.py
"""
from util.Square import CategorySquare, CenterSquare, RollAgainSquare
from util import squares

class Gameboard:
    """Class to model the Trival Compute game board as a graph.

    Attributes:
        squares (dict): stores gameboard squares by location ID

    Methods:
        initializeSquares
    """

    def __init__(self, squares:dict={}):
        self.squares = squares
        self.initializeSquares()

    def initializeSquares(self):
        """Function to build graph of Square vertices.
        """
        # 45 total squares in the board, so need 45 unique IDs

        # read map from squares.json
        for square in squares["squares"]:

            # check if center or roll again square
            if not square["color"]:
                if len(square["neighbors"]) == 4: # center
                    newSquare = CenterSquare(
                        id = square["id"],
                        players = [],
                        neighbors = square["neighbors"])
                else: # roll again
                    newSquare = RollAgainSquare(
                        id = square["id"],
                        players = [],
                        neighbors = square["neighbors"])

            else: # category square
                newSquare = CategorySquare(
                    id = square["id"],
                    players = [],
                    neighbors = square["neighbors"],
                    color = square["color"])

                if len(square["neighbors"]) == 3: # HQ 
                    newSquare.setIsHQ(True)

            self.squares[square["id"]] = newSquare
