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


def pgn2array(pgn: str) -> np.ndarray:
    """Converts a string PGN to a 2D numpy array which can be used later to
    select white or black moves

    :param pgn: string containing pgn
    :type pgn: str
    :return: numpy array where first column represents white move and second column black moves.
    Whenever black hasn't moved, the empty string "" represents absence of move.
    :rtype: np.ndarray
    """

    # Remove the result from the PGN, because we are only interested in moves
    pgn_moves = re.sub("(1-0)|(0-1)|(1/2-1/2)", "", pgn)

    # We split by each move, for example: '1.', '2.', etc.
    pgn_parsed = re.split(" ?[0-9]+\. ?", pgn_moves)
    pgn_parsed[0] = BEGINNING_OF_GAME_TOKEN
    pgn_parsed.append(END_OF_GAME_TOKEN)

    # Split moves so that each move is a list of strings. So a move is a list ['e4', 'e5']
    pgn_parsed = [move.strip().replace("  ", " ") for move in pgn_parsed]
    moves = [move.split(" ") for move in pgn_parsed]

    # If black didn't play, pad the move with the empty string ""
    moves_padded = [
        (
            move + [""]
            if len(move) == 1
            and move[0] not in [END_OF_GAME_TOKEN, BEGINNING_OF_GAME_TOKEN]
            else move
        )
        for move in moves
    ]

    # Convert to numpy array because it will be easier to slice
    moves_padded_array = np.array(moves_padded[1:-1])

    return moves_padded_array


def get_positions_with_white(
    pgn: str,
    seed: int = 42,
    n_positions=GAMES_SAMPLE,
    special_tokens=(BEGINNING_OF_GAME_TOKEN, END_OF_GAME_TOKEN),
) -> list[tuple[str | np.ndarray, str]]:
    """Generates a set of positions from a game where the player is white

    :param pgn: PGN representation of the game
    :type pgn: pgn
    :param seed: seed for sampling positions, defaults to 42
    :type seed: int, optional
    :return: list of random positions within the game. All elements are tuples of size 2,
    where the first element of the tuple are the moves played up to a certain point and the
    second element of the tuple is the next move white makes.
    :rtype: list[tuple[str | np.ndarray, str]]
    """
    moves_array = pgn2array(pgn)

    # Sample positions from the game, selecting the unique ones only and sorting to ensure reproducibility
    np.random.seed(seed)
    moves_samples = np.random.randint(0, moves_array.shape[0], n_positions)
    moves_samples = np.sort(np.unique(moves_samples))

    sample_positions = []
    for sample in moves_samples:
        # When it's the beginning of the game, use Beginning of Game as first move and opening as next one
        if sample == 0:
            position_sample = (special_tokens[0], moves_array[0, 0])

        # In the usual case, slice all the moves up to a certain point
        else:
            position_sample = (
                moves_array[0:sample, :],
                moves_array[sample, 0],
            )
        sample_positions.append(position_sample)

    return sample_positions


def get_positions_with_black(
    pgn: str,
    seed: int = 42,
    n_positions=GAMES_SAMPLE,
    special_tokens=(BEGINNING_OF_GAME_TOKEN, END_OF_GAME_TOKEN),
) -> list[tuple[str | np.ndarray, str]]:
    """Generates a set of positions from a game where the player is white

    :param pgn: PGN representation of the game
    :type pgn: pgn
    :param seed: seed for sampling positions, defaults to 42
    :type seed: int, optional
    :return: list of random positions within the game. All elements are tuples of size 2,
    where the first element of the tuple are the moves played up to a certain point and the
    second element of the tuple is the next move white makes.
    :rtype: list[tuple[str | np.ndarray, str]]
    """
    moves_array = pgn2array(pgn)
    pass


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
