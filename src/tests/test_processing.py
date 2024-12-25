import numpy as np
import pandas as pd
import pytest

from src.extraction.processing import (
    get_positions_with_black,
    get_positions_with_white,
    merge_data,
    pgn2array,
)

from .testing import (
    test_black_positions,
    test_games_dict,
    test_pgns,
    test_player_games,
    test_white_positions,
)


@pytest.fixture
def player_games():
    return pd.DataFrame(test_player_games)


@pytest.fixture
def games_data():
    return pd.DataFrame(test_games_dict)


def test_merge_data(player_games: pd.DataFrame, games_data: pd.DataFrame):
    player_games_data = merge_data(player_games, games_data)
    expected_new_cols = ["game_type", "fens", "pgn", "result"]

    assert all([col in player_games_data.columns for col in expected_new_cols])
    assert player_games_data.shape[0] == 2
    assert player_games["result"].isna().sum() == 0


@pytest.mark.parametrize("test_pgn,expected", test_pgns)
def test_pgn2array(test_pgn, expected):
    pgn_padded = pgn2array(test_pgn)
    print(pgn_padded)

    assert len(pgn_padded) == expected[0]
    assert (pgn_padded == expected[1]).all()
    assert isinstance(pgn_padded, np.ndarray)
    assert all(len(move) == 2 for move in pgn_padded)


@pytest.mark.parametrize(
    "input_data,expected",
    test_white_positions,
)
def test_get_positions_with_white(input_data, expected):
    test_pgn, n_positions = input_data
    white_positions = get_positions_with_white(
        test_pgn, seed=0, n_positions=n_positions, special_tokens=("<BOG>", "<EOG>")
    )
    for position, expected_position in zip(white_positions, expected, strict=True):
        assert (
            position[0] == expected_position[0]
            if isinstance(position[0], str)
            else (position[0] == expected_position[0]).all()
        )

        assert position[1] == expected_position[1]


@pytest.mark.parametrize(
    "input_data,expected",
    test_black_positions,
)
def test_get_positions_with_black(input_data, expected):
    test_pgn, n_positions = input_data
    black_positions = get_positions_with_black(
        test_pgn, seed=0, n_positions=n_positions, special_tokens=("<BOG>", "<EOG>")
    )
    for position, expected_position in zip(black_positions, expected, strict=True):
        assert (
            position[0] == expected_position[0]
            if isinstance(position[0], str)
            else (position[0] == expected_position[0]).all()
        )

        assert position[1] == expected_position[1]
