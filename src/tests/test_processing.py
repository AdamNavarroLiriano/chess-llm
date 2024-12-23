import numpy as np
import pandas as pd
import pytest

from src.extraction.processing import get_positions_with_white, merge_data, pad_pgn

from .testing import games_dict, pgns


@pytest.fixture
def player_games():
    data = [
        {
            "game": "A vs B",
            "result": "1-0",
            "year": 2024,
            "gid": "1",
            "is_white": False,
        },
        {
            "game": "B vs A",
            "result": "1/2-1/2",
            "year": 2024,
            "gid": "2",
            "is_white": True,
        },
    ]

    return pd.DataFrame(data)


@pytest.fixture
def games_data():
    return pd.DataFrame(games_dict)


@pytest.fixture
def games_pgn():
    return pgns


def test_merge_data(player_games: pd.DataFrame, games_data: pd.DataFrame):
    player_games_data = merge_data(player_games, games_data)
    expected_new_cols = ["game_type", "fens", "pgn", "result"]

    assert all([col in player_games_data.columns for col in expected_new_cols])
    assert player_games_data.shape[0] == 2
    assert player_games["result"].isna().sum() == 0


@pytest.mark.parametrize("test_pgn,expected", pgns)
def test_pad_pgn(test_pgn, expected):
    pgn_padded = pad_pgn(test_pgn)
    print(pgn_padded)

    assert len(pgn_padded) == expected[0]
    assert (pgn_padded == expected[1]).all()
    assert isinstance(pgn_padded, np.ndarray)
    assert all(len(move) == 2 for move in pgn_padded)


@pytest.mark.parametrize(
    "input_data,expected",
    [
        (("1. e4 1-0", 5), [("<BOG>", "e4")]),
        (("1. e4 e5 2. d4 1-0", 5), [("<BOG>", "e4"), ("<BOG> e4 e5", "e4")]),
    ],
)
def test_get_positions_with_white(input_data, expected):
    test_pgn, n_positions = input_data
    white_positions = get_positions_with_white(
        test_pgn, seed=0, n_positions=n_positions, special_tokens=("<BOG>", "<EOG>")
    )

    assert white_positions == expected
