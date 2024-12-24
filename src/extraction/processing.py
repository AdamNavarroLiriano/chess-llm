import re

import numpy as np
import pandas as pd

GAMES_SAMPLE = 5
BEGINNING_OF_GAME_TOKEN = "<BOG>"
END_OF_GAME_TOKEN = "<EOG>"


def merge_data(
    player_games_input: pd.DataFrame, games_data_input: pd.DataFrame
) -> pd.DataFrame:
    """Merges game data with player games

    :param player_games_input: game information for a player
    :type player_games_input: pd.DataFrame
    :param games_data_input: fens and pgn for a game
    :type games_data_input: pd.DataFrame
    :return: game data merged with its metadata
    :rtype: pd.DataFrame
    """
    games_data = games_data_input.copy()
    player_games = player_games_input.copy()

    # Merge by GID
    games_data = player_games.merge(games_data, on="gid")
    games_data.loc[:, ["fens", "game_type", "pgn"]] = (
        games_data["data"].apply(pd.Series).drop(columns=["result"])
    )

    games_data = games_data.drop(columns="data")
    games_data["pgn"] = games_data["pgn"].str.replace("\n", " ")

    # Remove the score from the pgn
    games_data["pgn"] = games_data["pgn"].str.replace(
        "( 1-0)|( 0-1)|( 1/2-1/2)", "", regex=True
    )

    return games_data


def get_positions_with_white(
    game: pd.Series, seed: int = 42
) -> list[tuple[np.ndarray, str]]:
    """Generates a set of positions from a game where the player is white

    :param game: Game containing PGN
    :type game: pd.Series
    :param seed: seed for sampling positions, defaults to 42
    :type seed: int, optional
    :return: list of random positions within the game
    :rtype: list[tuple[np.ndarray, str]]
    """
    pgn = game["pgn"]

    # Add special tokens to game for easier parsing
    pgn_parsed = re.split(" ?[0-9]+\. ", pgn)
    pgn_parsed[0] = BEGINNING_OF_GAME_TOKEN
    pgn_parsed.append(END_OF_GAME_TOKEN)

    # Split moves so that each move is a list of strings
    moves = [move.split(" ") for move in pgn_parsed]
    moves_padded = [
        (
            move + [""]
            if len(move) == 1
            and move[0] not in [END_OF_GAME_TOKEN, BEGINNING_OF_GAME_TOKEN]
            else move
        )
        for move in moves
    ]
    moves_padded_array = np.array(moves_padded[1:-1])

    # Sample positions from the game
    np.random.seed(seed)
    moves_samples = np.random.randint(0, len(moves_padded_array), GAMES_SAMPLE)

    sample_positions = []
    for sample in moves_samples:
        if sample == 0:
            position_sample = (BEGINNING_OF_GAME_TOKEN, moves_padded_array[0, 0])
        else:
            position_sample = (
                moves_padded_array[0 : (sample - 1), :],
                moves_padded_array[sample, 0],
            )
        sample_positions.append(position_sample)
    return sample_positions


if __name__ == "__main__":
    player_games = pd.read_parquet("../../data/player_games.parquet")
    games_data = pd.read_parquet("../../data/game_data.parquet")
    games_data = merge_data(
        player_games_input=player_games, games_data_input=games_data
    )

    player_games.head(2).to_dict(orient="records")
    games_data.head(2).to_json(orient="records")

    # Example when player is black
    black_games = games_data.loc[~games_data["is_white"]]
    game = black_games.iloc[2]
    fens = game["fens"]
    pgn = game["pgn"]
    pgn_parsed = re.split(" ?[0-9]+\. ", pgn)
    pgn_parsed[0] = BEGINNING_OF_GAME_TOKEN
    moves = [move.split(" ") for move in pgn_parsed]

    moves

    game
    moves

    np.random.seed(42)
    moves_samples = np.random.randint(0, len(moves), GAMES_SAMPLE)

    # edge case 0

    # normal cases

    moves_samples = [1]

    sample = moves_samples[0]

    array_moves = np.array(moves[1:])

    array_moves

    sample_positions = [
        (pgn_parsed[0 : max(2, sample)], moves[max(1, sample)][0])
        for sample in moves_samples
    ]

    sample_positions

    pgn_parsed[0:0]
