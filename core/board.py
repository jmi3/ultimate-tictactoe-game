from placeable import Placeable
from game_symbol import GameSymbol
from move import Move
from cell import Cell


class Board(Placeable):
    """
    Board class representing a multi-dimensional, recursive game board.
    Attributes:
        cells (list[list[Placeable]]): 2D list of cells or sub-boards.
        dimensions (tuple): Board size as (rows, columns).
        rows (int): Number of rows in the board.
        cols (int): Number of columns in the board.
        gameMoves (list[Move]): History of moves played on this board.
        symbol (GameSymbol): Current symbol representing the board's state (empty, full, or winner).
        winStreak (int): Number of consecutive symbols required to win on this board.

    """

    cells: list[list[Placeable]]

    def __init__(
        self,
        dimensions: tuple,
        cell_type: Placeable.__class__,
        cell_params: dict = {},
        winStreak: int = 3,
    ):
        self.dimensions = dimensions
        self.rows = dimensions[0]
        self.cols = dimensions[1]
        self.cells = [
            [cell_type(**cell_params) for _ in range(dimensions[1])]
            for _ in range(dimensions[0])
        ]
        for i in range(self.rows):
            for j in range(self.cols):
                self.cells[i][j].position = (i, j)
        self.gameMoves: list[Move] = []
        self.symbol = GameSymbol.empty
        self.winStreak = winStreak

    @classmethod
    def layers_init(cls, layers) -> "Board":
        """
        Initializes a multi-layered board structure based on the provided layer configurations.
        Args:
            layers (list of dict): A list of dictionaries, each specifying the configuration for a board layer.
                Each dictionary should contain:
                    - "dimensions" (tuple): The size of the layer (e.g., (3, 3)).
                    - "streak" (int): The number of consecutive marks needed to win at this layer.
        Returns:
            An instance of the class (cls) representing the initialized multi-layered board.
        Notes:
            - The first layer is initialized with basic cell types.
            - Subsequent layers are initialized recursively, nesting the previous layer as their cell type.
            - Assumes the existence of a 'Cell' class in the current scope.
        """

        def _params(dims, ct, cp, st):
            return {
                "dimensions": dims,
                "cell_type": ct,
                "cell_params": cp,
                "winStreak": st,
            }

        result = _params(layers[0]["dimensions"], Cell, {}, layers[0]["streak"])
        if len(layers) > 1:
            for layer in layers[1:]:
                result = _params(layer["dimensions"], cls, result, layer["streak"])
        return cls(**result)

    def __str__(self):
        return str(self.dimensions) + str(self.cells)

    def __getitem__(self, i):
        return self.cells[i]

    def __eq__(self, value):
        return self.cells == value.cells

    def _check_active_availability(self, active) -> list[bool]:
        """
        Recursively checks whether the specified 'active' path is available for play.

        Args:
            active (list): A list of coordinate pairs representing the path to check within the board's cells.

        Returns:
            list of bool: A list indicating, for each step in the path, whether the corresponding cell is available.
                - True if the cell is available for play.
                - False otherwise.

        Notes:
            - The method traverses the board recursively following the 'active' path.
            - Availability is determined based on the cell's symbol and position.
            - If the path is empty, returns whether the current cell is empty.
        """
        if len(active) == 0:
            return [self.symbol == GameSymbol.empty]
        if self.symbol == GameSymbol.empty:
            result = []
            if self.position:
                result.append(True)
            if active != []:
                result.extend(
                    self.cells[active[0][0]][active[0][1]]._checkActiveAvailability(
                        active[1:]
                    )
                )
            return result
        else:
            return [False]

    def make_move(self, move: Move) -> bool:
        """
        Attempts to make a move on the board at the specified position.
        Args:
            move (Move): The move to be made, containing the target position and sub-move details.
        Returns:
            bool: True if the move was successfully made.
        Raises:
            Exception: If the move is invalid (e.g., out of bounds, cell already occupied, or sub-move invalid).
        Notes:
            - Updates the board state with the new move.
            - Updates the winner symbol if the move results in a win.
            - Appends the move to the gameMoves history.
        """
        if self._is_in_board(move.position[0], move.position[1]):
            if (
                self.cells[move.position[0]][move.position[1]].symbol
                == GameSymbol.empty
            ):
                if self.cells[move.position[0]][move.position[1]].makeMove(
                    move.sub_move()
                ):
                    self.symbol = self.winner
                    self.gameMoves.append(move)
                    return True

        raise Exception(f"Invalid move {move} played")

    def undo_move(self, move: Move) -> None:
        """
        Reverts the most recent move on the board if it matches the provided move.

        Args:
            move (Move): The move to undo. Must be the most recent move played.

        Raises:
            Exception: If the provided move does not match the last move played.

        Notes:
            - Restores the previous symbol and updates the board state accordingly.
            - Only the most recent move can be undone.
        """
        if self.gameMoves[-1] == move:
            self.cells[move.position[0]][move.position[1]].undoMove(move.sub_move())
            self.symbol = self.winner
            self.gameMoves.pop()
        else:
            raise Exception(
                f"Unable to undo move {move}, last played move was {self.gameMoves[-1]}"
            )

    def final_symbol(self) -> GameSymbol:
        """
        Determines the final outcome of the game.
        Returns:
            GameSymbol: The winner of the game if there is one.
            GameSymbol.full: If the game ended in a draw (no empty cells left).
            None: If the game is still ongoing (no winner and empty cells remain).
        """
        temp = self.winner
        if temp != GameSymbol.empty:
            return temp
        temp = self.empty_cells
        if temp == 0:
            return GameSymbol.full
        return None

    @property
    def empty_cells(self) -> int:
        """Return number of empty cells in the board"""
        result = 0
        for row in self.cells:
            for cell in row:
                if cell.symbol == GameSymbol.empty:
                    result += 1
        return result

    @property
    def winner(self) -> GameSymbol:
        """Return winner of the board. If it returns GameSymbol.empty, no winner found"""
        result = GameSymbol.empty
        for row in self.cells:
            for cell in row:
                result = self._check_winner_from_pos(cell.position)
                if result != GameSymbol.empty:
                    return result
        if self.empty_cells == 0:
            return GameSymbol.full

        return result

    def sub_board(self, positions) -> Placeable:
        """
        Returns a sub-board or cell based on a list of positions.
        If the positions list is not empty, recursively traverses the board using the provided positions to access nested sub-boards or cells.
        If the positions list is empty, returns the current board (or calls the superclass implementation).
        Args:
            positions (list of tuple): A list of (row, column) tuples representing the path to the desired sub-board or cell.
        Returns:
            Placeable: The sub-board or cell at the specified position path.
        Raises:
            IndexError: If any position in the path is out of bounds.
        """

        if positions != []:
            return self.cells[positions[0][0]][positions[0][1]].subBoard(positions[1:])
        else:
            return super().sub_board(position=None)

    def _check_winner_from_pos(self, position, streak=None) -> GameSymbol:
        """
        Checks for a winning sequence of symbols starting from the given board position.

        Iterates in all four primary directions (horizontal, vertical, and both diagonals)
        from the specified position to determine if there is a contiguous sequence of the
        same non-empty symbol of length `self.winStreak`. Optionally, a custom streak length
        can be provided via the `streak` parameter.

        Args:
            position (tuple[int, int]): The (x, y) coordinates to start checking from.
            streak (int, optional): The length of the winning sequence to check for.
                If None, uses `self.winStreak`.

        Returns:
            GameSymbol: The symbol that forms a winning sequence if found; otherwise,
            returns `GameSymbol.empty`.
        """
        (x0, y0) = position
        ray_directions = [[1, 0], [0, 1], [1, 1], [1, -1]]
        for ray_direction in ray_directions:
            ray = self._dxdy_ray(x0, y0, *ray_direction, streak)
            count = 0
            prev_symbol = GameSymbol.empty
            for cell in ray:
                if cell.symbol != GameSymbol.empty and (
                    cell.symbol == prev_symbol or prev_symbol == GameSymbol.empty
                ):
                    count += 1
                else:
                    count = 0
                prev_symbol = cell.symbol
                if count == self.winStreak:
                    return prev_symbol
        return GameSymbol.empty

    def _is_in_board(self, x, y):
        """Checks if given coordinates are within the board's dimensions"""
        if not isinstance(x, int) or not isinstance(y, int):
            return False
        return x >= 0 and y >= 0 and x < self.rows and y < self.cols

    def _dxdy_ray(self, x0, y0, dx, dy, streak=None):
        """
        Returns a list of cell values forming a ray in a specified direction from a given starting point.
        The ray extends both forwards and backwards from (x0, y0) along the (dx, dy) direction,
        with a total length of 2 * streak (defaulting to self.winStreak if not specified).
        Only cells within the board boundaries are included.
        Args:
            x0 (int): The starting x-coordinate.
            y0 (int): The starting y-coordinate.
            dx (int): The x-direction increment for the ray.
            dy (int): The y-direction increment for the ray.
            streak (int, optional): The number of steps to extend in each direction from the starting point.
                If None, uses self.winStreak.
        Returns:
            list: A list of cell values along the ray within the board boundaries.
        """
        result = []
        if streak is None:
            streak = self.winStreak

        for i in range(-streak, streak):
            if self._is_in_board(x0 + i * dx, y0 + i * dy):
                result.append(self.cells[x0 + i * dx][y0 + i * dy])

        return result

    def get_empty_cells(self) -> Placeable:
        """
        Returns a list of positions of all empty cells on the board.
        Iterates through the board's cells and collects the positions of cells
        whose symbol is `GameSymbol.empty`.
        Returns:
            Placeable: A list of positions (or objects) representing empty cells.
        """
        result = []
        for row in self.cells:
            for cell in row:
                if cell.symbol == GameSymbol.empty:
                    result.append(cell.position)
        return result

    def get_valid_moves(
        self, active=None, first=True, desired_symbol=GameSymbol.empty
    ) -> list[Move]:
        """
        Generate a list of valid moves for the current board state.
        This method recursively determines all possible valid moves based on the current
        active cells, the board's winner status, and the desired symbol to be played.
        It supports both the initial call (first=True) and recursive calls for sub-boards.
        Args:
            active (Optional[list[tuple[int, int]]]): The list of active cell positions to consider for moves.
                If None, the method will determine the active cells automatically.
            first (bool): Indicates if this is the initial call (True) or a recursive call (False).
            desired_symbol (GameSymbol): The symbol to assign to moves at the top level (used only if first=True).
        Returns:
            list[Move]: A list of valid Move objects for the current board state.
        """
        if self.winner != GameSymbol.empty:
            return []
        if active is None:
            active = self.get_active()
        moves: list[Move] = []
        result = []
        eCellPositions = self.get_empty_cells()
        if first:
            try:
                active = active[
                    : self._check_active_availability(active=active).index(False)
                ]
            except Exception as e:
                pass

        if len(active) >= 1:
            moves = self.cells[active[0][0]][active[0][1]].getValidMoves(
                active[1:], first=False
            )
        else:
            for pos in eCellPositions:
                moves.extend(self.cells[pos[0]][pos[1]].getValidMoves(first=False))
        if first:
            for move in moves:
                if move.symbol == GameSymbol.empty:
                    move.symbol = desired_symbol
                    result.append(move)
        else:
            for move in moves:
                result.append(move.super_move([self.position]))
        return result

    def get_active(self):
        """
        Determines and returns the currently active positions based on the previous move.

        This method analyzes the last move in the game history (`self.gameMoves`) and uses its positions
        to compute which positions are currently active for the next move. If there are no moves yet,
        it returns an empty list. If not all positions are available (as determined by
        `_check_active_availability`), it returns the positions up to the first unavailable one.
        Otherwise, it returns all positions from the last move except the first.

        Returns:
            list: The list of currently active positions, or an empty list if no moves have been made.
        """
        if len(self.gameMoves) == 0:
            return []
        avail = self._check_active_availability(active=self.gameMoves[-1].positions[1:])
        if not all(avail):
            return self.gameMoves[-1].positions[1 : avail.index(False)]
        return self.gameMoves[-1].positions[1:]
