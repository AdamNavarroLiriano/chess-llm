import pandas as pd

from src.extraction.processing import (
    get_positions_with_black,
    get_positions_with_white,
    merge_data,
)

SEED = 42
N_POSITIONS = 12
BOG_TOKEN = "<BOG>"
EOG_TOKEN = "<EOG>"


def load_player_games_data() -> pd.DataFrame:
    player_games = pd.read_parquet("data/player_games.parquet")
    games_data = pd.read_parquet("data/game_data.parquet")
    games_data = merge_data(player_games, games_data)
    return games_data


if __name__ == "__main__":
    player_games_data = load_player_games_data()
    print(player_games_data.iloc[0])

    white_games = player_games_data[player_games_data["is_white"]].reset_index(
        drop=True
    )
    black_games = player_games_data[~player_games_data["is_white"]].reset_index(
        drop=True
    )

    # white_games["positions"] = white_games["pgn"].apply(
    #     lambda x: get_positions_with_white(
    #         x, seed=SEED, n_positions=N_POSITIONS, special_tokens=(BOG_TOKEN, EOG_TOKEN)
    #     )
    # )
    for i, pgn in enumerate(white_games["pgn"]):
        try:
            get_positions_with_white(
                pgn,
                seed=SEED,
                n_positions=N_POSITIONS,
                special_tokens=(BOG_TOKEN, EOG_TOKEN),
            )
        except:
            print(i)


