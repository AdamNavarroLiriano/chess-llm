import unittest
from unittest.mock import patch
from io import StringIO
from bs4 import BeautifulSoup
import chess
from ..extraction.extraction import PageGames, GameScrapper, PlayerGames


class TestPageGames(unittest.TestCase):
    def setUp(self):
        self.pid = 123
        self.page_number = 2
        self.page_games = PageGames(self.pid, self.page_number)

    def test_html(self):
        with patch("requests.Session.get") as mock_get:
            mock_response = mock_get.return_value
            mock_response.status_code = 200
            mock_response.content = b"<html><body><table></table></body></html>"

            html = self.page_games.html

            mock_get.assert_called_once_with(
                f"https://www.chessgames.com/perl/chess.pl?page={self.page_number}&pid={self.pid}",
                headers={
                    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.0.0 Safari/537.36"
                },
            )
            self.assertIsInstance(html, BeautifulSoup)

    def test_process_games_table(self):
        with patch.object(
            self.page_games,
            "_html",
            new=BeautifulSoup(
                StringIO(
                    "<html><body><table><tr><th>Col1</th><th>Col2</th></tr><tr><td>Data1</td><td>Data2</td></tr></table></body></html>"
                ),
                "html.parser",
            ),
        ):
            games_df = self.page_games.process_games_table()

            expected_columns = ["Col1", "Col2"]
            self.assertEqual(list(games_df.columns), expected_columns)
            self.assertEqual(len(games_df), 1)
            self.assertEqual(games_df.iloc[0].tolist(), ["Data1", "Data2"])

    def test_extract_games_links(self):
        with patch.object(
            self.page_games,
            "_html",
            new=BeautifulSoup(
                StringIO(
                    '<html><body><table><tr><td><a href="game1.html">Game1</a></td><td><a href="game2.html">Game2</a></td></tr></table></body></html>'
                ),
                "html.parser",
            ),
        ):
            games_links = self.page_games.extract_games_links()

            expected_games_links = ["game1.html", "game2.html"]
            self.assertEqual(games_links, expected_games_links)


class TestPlayerGames(unittest.TestCase):
    def setUp(self):
        self.pid = 456
        self.page_numbers = [1, 2, 3]
        self.player_games = PlayerGames(self.pid, self.page_numbers)

    def test_pid(self):
        self.assertEqual(self.player_games.pid, 456)

    def test_page_numbers(self):
        self.assertEqual(self.player_games.page_numbers, [1, 2, 3])

    def test_get_player_games(self):
        with patch("extraction.PageGames.get_games_links") as mock_get_games_links:
            mock_get_games_links.return_value = ["game1.html", "game2.html"]

            games = self.player_games.get_player_games()

            mock_get_games_links.assert_called_once()
            self.assertEqual(games, ["game1.html", "game2.html"])


class TestGameScrapper(unittest.TestCase):
    def setUp(self):
        self.game = chess.Board()
        self.game_str = str(self.game)

    def test_game(self):
        game = GameScrapper(self.game_str)

        self.assertEqual(game.game, self.game)

    def test_html_game(self):
        with patch("requests.Session.get") as mock_get:
            mock_response = mock_get.return_value
            mock_response.status_code = 200
            mock_response.content = (
                b'<html><body><div class="game">Game content</div></body></html>'
            )

            html_game = GameScrapper(self.game_str).html_game

            mock_get.assert_called_once_with(
                f"https://www.chessgames.com/perl/chess.pl?gid={self.game.gid()}",
                headers={
                    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.0.0 Safari/537.36"
                },
            )
            self.assertEqual(html_game, '<div class="game">Game content</div>')

    def test_result(self):
        with patch.object(
            GameScrapper,
            "_html_game",
            new=BeautifulSoup(
                StringIO(
                    '<html><body><div class="game">1. e4 e5 2. Nf3 Nc6 3. Bb5</div></body></html>'
                ),
                "html.parser",
            ),
        ):
            game = GameScrapper(self.game_str)
            result = game.result()

            self.assertEqual(result, "1. e4 e5 2. Nf3 Nc6 3. Bb5")

    def test_game_type(self):
        with patch.object(
            GameScrapper,
            "_html_game",
            new=BeautifulSoup(
                StringIO(
                    '<html><body><div class="game">1. e4 e5 2. Nf3 Nc6 3. Bb5</div></body></html>'
                ),
                "html.parser",
            ),
        ):
            game = GameScrapper(self.game_str)
            game_type = game.game_type()

            self.assertEqual(game_type, "chess")


if __name__ == "__main__":
    unittest.main()
