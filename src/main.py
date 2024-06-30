from extraction.extraction import PlayerGames, PageGames, GameScrapper

PLAYER = "Magnus Carlsen"
MIN_YEAR = 2014
MAX_YEAR = 2024


def get_game_data(gid: str) -> tuple:
    game_scrapper = GameScrapper(gid)

    result = game_scrapper.result

    try:
        fens = game_scrapper.fens
    except:
        return None

    pgn = game_scrapper.pgn
    game_type = game_scrapper.game_type

    return {"result": result, "pgn": pgn, "game_type": game_type, "fens": fens}


def main():
    # Get player page
    player = PlayerGames(PLAYER)
    player_page = PageGames(player.pid, player.page_numbers)

    #  Get player games in date range
    player_games = player.get_player_games(max_year=MAX_YEAR, min_year=MIN_YEAR)

    return player_games


if __name__ == "__main__":
    player_games = main()
    player_games["data"] = player_games["gid"].apply(lambda x: get_game_data(x))
