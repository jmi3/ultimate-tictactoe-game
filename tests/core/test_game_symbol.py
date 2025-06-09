import pytest

from core.game_symbol import GameSymbol

def test_game_symbol_uniqueness():
    """
    Test that all GameSymbol attributes are unique.
    """
    symbols = [GameSymbol.__dict__[attr] for attr in GameSymbol.__dict__]
    assert len(symbols) == len(set(symbols)), "GameSymbol attributes are not unique"