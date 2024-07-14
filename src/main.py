import asyncio
import time

import pandas as pd

from extraction.extraction import GameScrapper, PageGames, PlayerGames

PLAYER = "Magnus Carlsen"
MIN_YEAR = 2014
MAX_YEAR = 2024


async def get_game_data(gid: str) -> dict[str, str | list[tuple[str]]]:
    """Gets data from a game, using the game id (gid)

    Args:
        gid (str): game id from chessgames.com website

    Returns:
        dict[str, str | list[tuple[str]]]: dictionary with game data or
        None if unable to get data
    """
    game_scrapper = GameScrapper(gid)

    result = await game_scrapper.result
    game_type = game_scrapper.game_type

    try:
        pgn = await game_scrapper.pgn
        fens = await game_scrapper.convert_to_fen()
    except:
        return None

    return (
        gid,
        {
            "pgn": pgn,
            "game_type": game_type,
            "fens": fens,
            "result": result,
        },
    )


async def main():
    # Get player page
    player = PlayerGames(PLAYER)

    #  Get player games in date range
    player_games = player.get_player_games(max_year=MAX_YEAR, min_year=MIN_YEAR)

    # Remove Blitz games, Simultaneous, Chess.com, 960 and lichess games
    events_out = "(blitz)|(bullet)|(simultaneous)|(simul)|(960)|(lichess)|(exhibition)|(speed)|(chess.com)|(fischer)|(titled)"
    player_games = player_games.loc[
        ~player_games["event/locale"].str.lower().str.contains(events_out, regex=True)
    ].reset_index(drop=True)

    # Export
    player_games = player_games.drop(columns="links")
    player_games.to_parquet("../data/player_games.parquet")

    # Get game data
    player_games = pd.read_parquet("../data/player_games.parquet")

    # Async gather pages. We do it batched to avoid timeout issues
    batch_size = 100
    gids = player_games["gid"].tolist()
    gid_batches = [gids[i : i + batch_size] for i in range(0, len(gids), batch_size)]

    # List that will store the results
    game_data_responses = []

    for batch_idx, gid_batch in enumerate(gid_batches):
        print(f"Batch {batch_idx + 1} of {len(gid_batches)}")

        game_data_tasks = []

        for gid in gid_batch:
            game_data_tasks.append(get_game_data(gid))

        batch_data = await asyncio.gather(*game_data_tasks)
        game_data_responses.append(batch_data)

        # Sleep for 120 seconds
        sleep_secs = 120
        print(f"Sleeping for {sleep_secs} seconds")
        time.sleep(sleep_secs)

    game_data_responses_unwrapped = [
        item for sublist in game_data_responses for item in sublist
    ]

    game_data_df = pd.DataFrame(game_data_responses_unwrapped, columns=["gid", "data"])
    game_data_df.to_parquet("../data/game_data.parquet", index=False)

    return player_games


if __name__ == "__main__":
    main()
