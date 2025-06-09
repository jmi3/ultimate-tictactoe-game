import pytest

from core.placeable import Placeable
from core.board import Board
from core.game_symbol import GameSymbol


class MockCell(Placeable):
    position: tuple = None

    def __init__(self, **kwargs):
        pass

def make_layer(dimensions, win_streak):
    return {"dimensions":tuple(dimensions), "streak":int(win_streak)}
    

def test_board_init_basic():
    board = Board(dimensions=(4, 5), cell_type=MockCell, cell_params={}, win_streak=3)

    assert board.rows == 4, "Board should have 4 rows"
    assert board.cols == 5, "Board should have 5 columns"
    assert len(board.cells) == 4, "Board should have 4 rows of cells"
    assert all(len(row) == 5 for row in board.cells), "Each row should have 5 cells"
    assert board.symbol == GameSymbol.empty, "Initial board symbol should be empty"
    assert board.win_streak == 3, "Win streak should be set to 3"
    # Check that all cells are instances of MockCell and have correct positions
    for i in range(4):
        for j in range(5):
            assert isinstance(board.cells[i][j], MockCell), f"Cell at ({i}, {j}) should be an instance of MockCell"
            assert board.cells[i][j].position == (i, j), f"Cell at ({i}, {j}) should have position ({i}, {j})"

def test_board_init_nested():
    params = {
        "dimensions": (4, 5),
        "cell_type": MockCell,
        "cell_params": {},
        "win_streak": 3,
    }
    board = Board(dimensions=(4, 5), cell_type=Board, cell_params=params, win_streak=3)

    assert board.rows == 4, "Board should have 4 rows"
    assert board.cols == 5, "Board should have 5 columns"
    assert len(board.cells) == 4, "Board should have 4 rows of cells"
    assert all(len(row) == 5 for row in board.cells), "Each row should have 5 cells"
    assert board.symbol == GameSymbol.empty, "Initial board symbol should be empty"
    assert board.win_streak == 3, "Win streak should be set to 3"
    # Check that all cells are instances of MockCell and have correct positions
    for i in range(4):
        for j in range(5):
            assert isinstance(board.cells[i][j], Board), f"Cell at ({i}, {j}) should be an instance of Board"
            assert board.cells[i][j].rows == 4, f"Board cell at ({i}, {j}) should have 4 rows"
            assert board.cells[i][j].cols == 5, f"Board cell at ({i}, {j}) should have 5 columns"
            assert board.cells[i][j].win_streak == 3, f"Board cell at ({i}, {j}) should have win streak of 3"
            assert board.cells[i][j].symbol == GameSymbol.empty, f"Board cell at ({i}, {j}) should have empty symbol"
            for k in range(4):
                for l in range(5):
                    assert isinstance(board.cells[i][j].cells[k][l], MockCell), f"Cell at ({i}, {j}) should contain MockCell at ({k}, {l})"
                    assert board.cells[i][j].cells[k][l].position == (k, l), f"Cell at Board.cells[{i}][{j}].cells[{k}][{l}] should have position ({k}, {l})"
            
def test_board_init_invalid_cell_type():
    with pytest.raises(TypeError, match="cell_type must be a subclass of Placeable, got <class 'int'>"):
        Board(dimensions=(4, 5), cell_type=int, cell_params={}, win_streak=3)

def test_board_layers_init():
    layers = [make_layer((4,5),3) for _ in range(2)]
    board = Board.layers_init(layers=layers, cell_type=MockCell, cell_params={})
    
    assert board.rows == 4
    assert board.cols == 5
    assert len(board.cells) == 4
    assert all(len(row) == 5 for row in board.cells)
    assert board.symbol == GameSymbol.empty
    assert board.win_streak == 3
    # Check that all cells are instances of MockCell and have correct positions
    for i in range(4):
        for j in range(5):
            assert isinstance(board.cells[i][j], Board)
            assert board.cells[i][j].rows == 4
            assert board.cells[i][j].cols == 5
            assert board.cells[i][j].win_streak == 3
            assert board.cells[i][j].symbol == GameSymbol.empty
            for k in range(4):
                for l in range(5):
                    assert isinstance(board.cells[i][j].cells[k][l], MockCell)
                    assert board.cells[i][j].cells[k][l].position == (k, l)



    