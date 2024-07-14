import re

import numpy as np
import pandas as pd

player_name = 'Magnus Carlsen'

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
        games_data["data"].apply(pd.Series).drop(columns=["result", "data"])
    )

    # Determine whether player is white or black


    return games_data


player_games = pd.read_parquet("../../data/player_games.parquet")
games_data = pd.read_parquet("../../data/game_data.parquet")

games_data = merge_data(player_games_input=player_games, games_data_input=games_data)


games_data['players'] = games_data['game'].str.replace('^[0-9\.]+', '', regex=True).str.strip().str.split(' vs ')

games_data
games_data['game'].str.split(' vs ').apply(lambda x: 1 if x[0] in player_name)