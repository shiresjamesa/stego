"""GameUtils.py
"""
import random
from util.Gameboard import Gameboard


class GameUtils:
    """Class to store utility functions for the game.

    Methods:
        roll: simulates roll of a single die

    """
    GAMEBOARD = Gameboard()

    @staticmethod
    def roll():
        """Function to simulate die roll.

        @returns int: value of roll

        """
        return random.randint(1, 6)

    @staticmethod
    def getPossibleMoves(currentSquareId:str, diceRoll:int)->list:
        """Function to compute all possible squares to move given dice roll
        using Breadth First Search.

        @param currentSquareId (str): location of current occupied square
        @param diceRoll (int): value of dice roll

        @returns list: list of square IDs for possible moves
        """
        visited = []
        result = []
        queue = [(currentSquareId, diceRoll)]

        while queue:
            curId, steps = queue.pop(0)

            if steps == 0 and curId not in result: # add to result
                result.append(curId)
                continue

            if curId not in visited:
                visited.append(curId)

            for neighborId in GameUtils.GAMEBOARD.squares[curId].getNeighbors():
                if neighborId not in visited and (neighborId, steps - 1) \
                not in queue: # "visit" next square

                    queue.append((neighborId, steps - 1))

        if currentSquareId in result:
            result.remove(currentSquareId)
        return result








