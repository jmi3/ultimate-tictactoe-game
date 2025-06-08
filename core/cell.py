from game_symbol import GameSymbol
from move import Move
from placeable import Placeable

from typing import List


class Cell(Placeable):
    """
    Represents a single cell in the game board, capable of holding a symbol.
    A `Cell` is the simplest unit of placement in the game. It tracks its symbol (such as X, O, or empty)
    and provides methods for making and undoing moves, checking for a winner, and determining valid moves.
    Attributes:
        dimensions (tuple): The size of the cell, always (1, 1).
        symbol (GameSymbol): The current symbol in the cell (e.g., X, O, or empty).
    Methods:
        __str__(): Returns the string representation of the cell's symbol.
        __eq__(value): Checks equality based on position and symbol.
        make_move(move): Places a symbol in the cell according to the move.
        undo_move(move): Removes the symbol if it matches the move's symbol.
        winner: Property returning the symbol as the winner (or empty if none).
        _check_active_availability(active): Checks if the cell is available for a move.
        get_valid_moves(active, first): Returns a list of valid moves for this cell.
    """

    def __init__(self) -> None:
        self.dimensions = (1, 1)
        self.symbol = GameSymbol.empty

    def __str__(self) -> str:
        return str(self.symbol)

    def __eq__(self, value):
        return self.position == value.position and self.symbol == value.symbol

    def make_move(self, move: Move) -> bool:
        """
        Place a symbol in the cell according to the move.
        """
        if self.symbol != GameSymbol.empty:
            return False
        self.symbol = move.symbol
        return True

    def undo_move(self, move: Move):
        """
        Remove the symbol from the cell if it matches the move's symbol.
        """
        if self.symbol == move.symbol:
            self.symbol = GameSymbol.empty
            return True
        return False

    @property
    def winner(self):
        """Return winner of the board. If GameSymbol.empty returned, no winner was found"""
        return self.symbol

    def _check_active_availability(self, active=None) -> List[bool]:
        """
        Checks if the cell is available for activation.
        Args:
            active (optional): An optional parameter that may be used to specify the active state. On Cell level, it is not used.
        Returns:
            List[bool]: [True] if the cell's symbol is empty (i.e., the cell is available), [False] otherwise.
        """
        return [self.symbol == GameSymbol.empty]

    def get_valid_moves(self, active=[], first=True):
        """
        Returns a list of valid moves for the current cell.
        If the cell is empty, returns a list containing a single Move object representing
        the possible move at this cell's position. Otherwise, returns an empty list.

        Args (all unused on Cell level):
            active (list, optional): A list of currently active cells or positions. Defaults to [].
            first (bool, optional): Indicates if this is the first move in a sequence. Defaults to True.
        Returns:
            list[Move]: A list of valid Move objects for this cell, which is only one Move containing the cell's position and empty symbol.
        """

        if self.symbol == GameSymbol.empty:
            return [Move([self.position], self.symbol)]
