import pandas as pd
import numpy as np
import requests
from bs4 import BeautifulSoup


def find_player_pid(player_name: str) -> str | None:
    """
    Finds the player's ID (pid) on the Chessgames.com website.

    Args:
        player_name (str): The name of the player.

    Returns:
        str | None: The link to the player's profile page if found, None otherwise.
    """

    url_search = f"https://www.chessgames.com/perl/ezsearch.pl?search={player_name}"

    with requests.Session() as s:
        r = s.get(
            url_search,
            headers={
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.0.0 Safari/537.36"
            },
        )
        html_search = BeautifulSoup(r.content, "html.parser")

    # Get all links and filter by the one that contains the player's id (pid)
    links = html_search.find_all("a")
    player_profile = [
        link["href"] for link in links if "chessplayer?pid" in link["href"]
    ][0]

    return player_profile
