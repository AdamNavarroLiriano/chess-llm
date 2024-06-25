import pandas as pd
import requests
from bs4 import BeautifulSoup
import io


class PageGames:
    """Games for a given player's page in chess games"""

    def __init__(
        self,
        pid: int,
        page_number: int,
    ) -> None:
        self.pid = pid
        self.page_number = page_number
        self._html = None

    @property
    def html(self) -> BeautifulSoup:
        """HTML of the page

        Returns:
            BeautifulSoup: html of the page containing a player's games
        """
        if self._html is None:
            page_url = f"https://www.chessgames.com/perl/chess.pl?page={self.page_number}&pid={self.pid}"

            with requests.Session() as s:
                r = s.get(
                    page_url,
                    headers={
                        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.0.0 Safari/537.36"
                    },
                )
                self._html = BeautifulSoup(r.content, "html.parser")

        return self._html

    def process_games_table(self) -> pd.DataFrame:
        """Extracts games from a player's page

        Returns:
            pd.DataFrame: DataFrame with details of the player's games
        """

        # The table at index 1 contains the player's games
        table_html = str(self.html.find_all("table")[1])

        # Reorganize the table so that it is easier to read
        games_df = pd.read_html(io.StringIO(table_html))[2]
        games_df.columns = games_df.loc[0]
        games_df = games_df.loc[1:].reset_index(drop=True)

        return games_df

    def extract_games_links(self) -> list:
        """Extracts links to games from a player's page

        Returns:
            list: List of links to games
        """

        games_links = [
            game
            for game in self.html.find_all("a")
            if "chessgame?gid=" in game["href"] and game.find("img") is None
        ]

        return games_links


class PlayerGames:
    def __init__(self, player_name: str) -> None:
        self.player_name = player_name
        self._pid = None
        self._page_numbers = None

    @property
    def pid(self) -> int:
        """
        The player's ID (pid) on the Chessgames.com website.

        Returns:
            int: The id for the player, if found.
        """
        if self._pid is None:
            url_search = (
                f"https://www.chessgames.com/perl/ezsearch.pl?search={self.player_name}"
            )

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
            pid_ref = [
                link["href"] for link in links if "chessplayer?pid" in link["href"]
            ][0]

            self._pid = int(pid_ref.split("pid=")[-1])

        return self._pid

    @property
    def page_numbers(self) -> int:
        """
        Number of player's pages of games on the Chessgames.com website.

        Returns:
        int: The number of pages of games found for a given player
        """
        if self._page_numbers is None:
            base_url = (
                f"https://www.chessgames.com/perl/chess.pl?page={1}&pid={self.pid}"
            )

            with requests.Session() as s:
                r = s.get(
                    base_url,
                    headers={
                        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.0.0 Safari/537.36"
                    },
                )
                html = BeautifulSoup(r.content, "html.parser")

            table_games = str(html.find_all("table")[1])

            page_numbers = pd.read_html(io.StringIO(table_games))[0]
            page_numbers = int(page_numbers[0].iloc[0].split(";")[0].split("of ")[1])
            self._page_numbers = page_numbers

        return self._page_numbers

    def get_player_games(
        self, max_year: int | None, min_year: int | None
    ) -> pd.DataFrame:
        """Finds a player's games in a given year range

        Args:
            max_year (int | None): maximum year to consider for a player's games
            min_year (int | None): minimum year to consider for a player's games

        Returns:
            pd.DataFrame: DataFrame containing games, details and links to it for the player
        """

        player_games = pd.DataFrame()

        if max_year is not None and min_year is not None:
            assert (
                max_year >= min_year
            ), '"max_year" must be greater than or equal to "min_year"'

        for page_number in range(self.page_numbers, 0, -1):
            page = PageGames(self.pid, page_number)

            games_df = page.process_games_table()
            games_df["links"] = page.extract_games_links()

            # We ensure that the games are in the correct range, if not, we break the loop
            games_df["Year"] = games_df["Year"].astype(int)

            lower_bound_cond = (
                games_df["Year"] >= min_year if min_year is not None else True
            )
            upper_bound_cond = (
                games_df["Year"] <= max_year if max_year is not None else True
            )

            games_df = games_df.loc[(lower_bound_cond) & (upper_bound_cond)]

            if games_df.shape[0] == 0:
                break

            player_games = pd.concat([player_games, games_df], ignore_index=True)

        return player_games


if __name__ == "__main__":
    magnus = PlayerGames("Magnus Carlsen")

    magnus_page = PageGames(magnus.pid, magnus.page_numbers)

    games_df = magnus_page.process_games_table()
    games_links = magnus_page.extract_games_links()

    magnus_games = magnus.get_player_games(max_year=None, min_year=2023)

    assert games_df.shape[0] == len(games_links)
