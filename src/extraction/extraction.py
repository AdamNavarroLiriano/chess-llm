import pandas as pd
import requests
from bs4 import BeautifulSoup
import io
import chess
import chess.pgn
from typing import TextIO
import re
import aiohttp


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

        # Final preprocessing
        player_games = player_games.dropna(axis=1)
        player_games.columns = [
            col.lower().replace(" ", "_") for col in player_games.columns
        ]

        player_games["url"] = "https://www.chessgames.com/" + player_games[
            "links"
        ].apply(lambda x: x["href"])

        player_games["gid"] = player_games["url"].str.split("gid=").str[-1]

        return player_games


class GameScrapper:
    """Scrapes games, PGN files, and information from chessgames.com"""

    def __init__(self, gid: str) -> None:
        self.gid = gid
        self._game = None
        self._html = None

    @property
    async def game(self) -> chess.pgn.Game:
        """Creates a chess.pgn.Game object from a PGN string

        Returns:
            chess.pgn.Game: object that stores result, FENs and PGN string for entire game
        """
        if self._game is None:
            pgn_buffer = await self._get_pgn_from_url()
            self._game = chess.pgn.read_game(pgn_buffer)

        return self._game

    @property
    def html_game(self) -> BeautifulSoup:
        if self._html is None:
            self._html = self._get_game_data()

        return self._html

    @property
    def result(self) -> str:
        """Retruns the result of the match

        Returns:
            str: 1-0, 0-1 or 1/2-1/2
        """
        return self.game.headers["Result"]

    @property
    def game_type(self) -> str | None:
        """Returns the game type (BLITZ, CLASSICAL, ARMAGGEDON, RAPID, etc.)

        Returns:
            str | None: game type (time control) if not None. None otherwise
        """

        html_game = self.html_game

        try:
            game_type = html_game.find(class_="gametype_cs_notice").text

            time_control = re.search(
                "This game is type: ([A-Za-z]+). ", game_type
            ).groups()[0]

            return time_control

        except AttributeError:
            return None

    @property
    async def pgn(self) -> str:
        """PGN for the entire game in algebraic notation

        Returns:
            str: PGN part of the game
        """
        game = await self.game
        exporter = chess.pgn.StringExporter(headers=False)
        pgn_string = game.accept(exporter)
        return pgn_string

    async def convert_to_fen(self) -> list[tuple[str]]:
        """Converts a game into a list of tuples of FENs

        Returns:
            list[tuple[str]]: containing all positions reached in the game,
            starting from the first move
        """
        fens = []
        game = await self.game
        while game.next():
            fens.append(game.board().fen())
            game = game.next()

        # Drop the first FEN because its the starting position
        fens = fens[1:]

        # Pair FENs my move. So the list will contain tuples of FEN
        fens = list(zip(fens[::2], fens[1::2]))

        return fens

    async def _get_pgn_from_url(self) -> TextIO:
        """Reads PGN from a URL

        Returns:
            TextIO: string buffer for the game.
        """

        url_pgn = (
            f"https://www.chessgames.com/nodejs/game/viewGamePGN?text=1&gid={self.gid}"
        )

        async with aiohttp.ClientSession() as s:

            async with s.get(
                url_pgn,
                headers={
                    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.0.0 Safari/537.36"
                },
            ) as r:
                text = await r.text()
                return io.StringIO(text)

    async def _get_game_data(self) -> BeautifulSoup:

        url_game = f"https://www.chessgames.com/perl/chessgame?gid={self.gid}"

        async with aiohttp.ClientSession() as s:
            async with s.get(
                url_game,
                headers={
                    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.0.0 Safari/537.36"
                },
            ) as r:
                html_text = await r.text()
                return BeautifulSoup(html_text, "html.parser")
