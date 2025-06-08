class Placeable:
    """
    Each placeabe inherits from this class. It carries just it's position
    """

    position = None

    def make_move(self, move):
        pass

    def undo_move(self, move):
        pass

    def sub_board(self, position):
        return self

    def get_valid_moves(self, active=[]):
        pass
