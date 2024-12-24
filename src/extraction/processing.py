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


def pad_pgn(pgn: str) -> np.ndarray:
    # Add special tokens to game for easier parsing
    # pgn =  "1. d4 Nf6 2. c4 e6 3. Nc3 d5 4. cxd5 exd5 5. Bg5 Be7 6. e3 h6 7. Bh4 Bg4 8. f3\\nBe6 9. Bd3 c5 10. Nge2 Nc6 11. O-O O-O 12. Re1 Re8 13. Bc2 Rc8 14. Nf4 cxd4 15.\\nNxe6 fxe6 16. exd4 Nxd4 17. Bg6 Rf8 18. Bf2 Nc6 19. Rxe6 d4 20. Ne2 Bc5 21. Nf4\\nNd5 22. Qb3 Nxf4 23. Rd6+ Kh8 24. Rxd8 Rcxd8 25. Qxb7 Ne5 26. Be4 Bb6 27. a4\\nNc4 28. Qa6 Nd2 29. a5 Bc5 30. Bb7 Nb3 31. Rd1 d3 32. Bxc5 Nxc5 33. Qxa7 Nxb7\\n34. Qxb7 Rfe8 35. g3 d2 36. Qb4 Rd4 37. Qxd2 Rxd2 38. Rxd2 Ne6 39. b4 Kg8 40.\\nb5 Ra8 41. Ra2 Kf7 42. Kf2 Ke7 43. b6 Nc5 44. Ke3 Kd6 45. Kf4 g6 46. h4 Kd5 47.\\nKg4 Kc6 48. h5 Rg8 49. Rc2 Kb5 50. hxg6 Rxg6+ 51. Kh5 1-0"

    # Remove the result from the PGN, because we are only interested in moves
    pgn_moves = re.sub("(1-0)|(0-1)|(1/2-1/2)", "", pgn)

    # We split by each move, for example: '1.', '2.', etc.
    pgn_parsed = re.split(" ?[0-9]+\. ?", pgn_moves)
    pgn_parsed[0] = BEGINNING_OF_GAME_TOKEN
    pgn_parsed.append(END_OF_GAME_TOKEN)

    # Split moves so that each move is a list of strings
    pgn_parsed = [move.strip().replace("  ", " ") for move in pgn_parsed]
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

    return moves_padded_array


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
    moves_padded_array = pad_pgn(pgn)

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
