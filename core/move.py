from core.game_symbol import GameSymbol


class Move:
    """
    Represents a move.
    Attributes:
        positions (list[tuple]): A list of positions representing the move's path through the board hierarchy.
        position (tuple): The first position in the positions list, if available.
        symbol (GameSymbol): The symbol (e.g., X or O) associated with the move.
        isDecisive (bool): Indicates if the move is decisive (class-level attribute).
    Methods:
        __init__(positions, symbol):
            Initializes a Move with a list of positions and a symbol.
        __eq__(value):
            Checks equality with another Move based on positions and symbol.
        __str__():
            Returns a string representation of the move.
        str_pos(pos):
            Converts a list of positions to their string representations.
        sub_board():
            Returns the current move (placeholder for sub-board logic).
        sub_move():
            Returns a new Move representing the next level in the positions hierarchy.
        super_move(superMove):
            Returns a new Move with superMove prepended to the positions list.
    """

    isDecisive: bool

    def __init__(self, positions: list[tuple], symbol: GameSymbol) -> None:
        self.positions = positions
        if positions is not None:
            self.position = positions[0]
        self.symbol = symbol

    def __eq__(self, value: object) -> bool:
        if value is None:
            return False
        return (value.positions == self.positions) and (value.symbol == self.symbol)

    def __str__(self) -> str:
        return f"{self.symbol}:{'>'.join(self.str_pos(self.positions))}"

    def str_pos(self, pos: list[tuple]) -> list[str]:
        """
        Converts each element in the given position iterable to its string representation.
        Args:
            pos (iterable): An iterable containing elements to be converted to strings.
        Returns:
            list: A list of string representations of the elements in `pos`.
        """

        result = []
        for i in range(len(pos)):
            result.append(str(pos[i]))
        return result

    def sub_move(self):
        """
        Returns a new Move object representing the next sub-move in the sequence.

        If there is only one position left in the current move, returns a Move with positions set to None.
        Otherwise, returns a Move with the first position removed from the positions list.

        Returns:
            Move: A new Move object representing the next sub-move.
        """
        if len(self.positions) == 1:
            return Move(positions=None, symbol=self.symbol)
        return Move(positions=self.positions[1:], symbol=self.symbol)

    def super_move(self, superMove: list[tuple]) -> "Move":
        """
        Creates a new Move object by combining the given superMove positions with the current move's positions.

        If the current move has no positions, returns a Move with only the superMove positions.
        Otherwise, returns a Move with the superMove positions prepended to the current positions.

        Args:
            superMove (list): A list of positions representing the super move to be combined.

        Returns:
            Move: A new Move object with the combined positions and the current symbol.
        """
        if len(self.positions) == 0:
            return Move(positions=superMove, symbol=self.symbol)
        return Move(positions=[*superMove, *self.positions], symbol=self.symbol)
