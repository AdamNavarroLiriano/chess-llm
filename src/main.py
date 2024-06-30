from extraction.extraction import PlayerGames, PageGames, GameScrapper
import time
import random
from multiprocessing import Pool
import pandas as pd
import os

PLAYER = "Magnus Carlsen"
MIN_YEAR = 2014
MAX_YEAR = 2024


def get_game_data(gid: str) -> dict[str, str | list[tuple[str]]]:
    """Gets data from a game, using the game id (gid)

    Args:
        gid (str): game id from chessgames.com website

    Returns:
        dict[str, str | list[tuple[str]]]: dictionary with game data or
        None if unable to get data
    """
    game_scrapper = GameScrapper(gid)

    result = game_scrapper.result
    game_type = game_scrapper.game_type

    try:
        pgn = game_scrapper.pgn
        fens = game_scrapper.convert_to_fen()
    except:
        return None

    time.sleep(random.uniform(3, 10))

    return (gid, {"result": result, "pgn": pgn, "game_type": game_type, "fens": fens})


def main():
    # Get player page
    player = PlayerGames(PLAYER)
    player_page = PageGames(player.pid, player.page_numbers)

    #  Get player games in date range
    player_games = player.get_player_games(max_year=MAX_YEAR, min_year=MIN_YEAR)

    return player_games


if __name__ == "__main__":
    player_games = main()

    # Remove Blitz games, Simultaneous, Chess.com, 960 and lichess games
    events_out = "(blitz)|(bullet)|(simultaneous)|(simul)|(960)|(lichess)|(exhibition)|(speed)|(chess.com)|(fischer)|(titled)"
    player_games = player_games.loc[
        ~player_games["event/locale"].str.lower().str.contains(events_out, regex=True)
    ].reset_index(drop=True)

    # Export
    player_games = player_games.drop(columns="links")

    # Get game data
    player_games.to_parquet("../data/player_games.parquet")
    player_games = pd.read_parquet("../data/player_games.parquet")

    with Pool(8) as p:
        game_data = p.map(get_game_data, player_games["gid"].tolist())
