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
        "( 1-0)|( 0-1)|( 1/2-1/2)", '', regex=True
    )

    return games_data


player_games = pd.read_parquet("../../data/player_games.parquet")
games_data = pd.read_parquet("../../data/game_data.parquet")
games_data = merge_data(player_games_input=player_games, games_data_input=games_data)

# Example of processing white moves
white_games = games_data.loc[games_data["is_white"]]
game = white_games.iloc[1]
fens = game["fens"]
pgn = game["pgn"]
pgn_parsed = re.split(" ?[0-9]+\. ", pgn)

pgn_parsed[0] = BEGINNING_OF_GAME_TOKEN
pgn_parsed.append(END_OF_GAME_TOKEN)

moves = [move.split(" ") for move in pgn_parsed]
moves_padded = [move + [''] if len(move)==1 and move[0] not in [END_OF_GAME_TOKEN, BEGINNING_OF_GAME_TOKEN] else move
                for move in moves ]

moves_padded

np.random.seed(42)
moves_samples = np.random.randint(0, len(moves), GAMES_SAMPLE)
sample_positions = [
    (pgn_parsed[0 : max(1, sample)], moves[max(1, sample)][0])
    for sample in moves_samples
]



# Example when player is black
black_games = games_data.loc[~games_data["is_white"]]
game = black_games.iloc[2]
fens = game["fens"]
pgn = game["pgn"]
pgn_parsed = re.split(" ?[0-9]+\. ", pgn)
pgn_parsed[0] = BEGINNING_OF_GAME_TOKEN
moves = [move.split(" ") for move in pgn_parsed]


np.random.seed(42)
moves_samples = np.random.randint(0, len(moves), GAMES_SAMPLE)


moves_samples = [0]


# edge case 0


# normal cases

moves_samples = [1]
sample = moves_samples[0]

array_moves = np.array(moves[1:])

array_moves[]


sample_positions = [
    (pgn_parsed[0 : max(2, sample)], moves[max(1, sample)][0])
    for sample in moves_samples
]

sample_positions

pgn_parsed[0:0]
