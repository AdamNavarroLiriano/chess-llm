from io import StringIO
from unittest.mock import patch

import chess
import pytest
from bs4 import BeautifulSoup

from ..extraction.extraction import GameScrapper, PageGames, PlayerGames


@pytest.fixture
def page_games():
    pid = 123
    page_number = 2
    return PageGames(pid, page_number)


@pytest.fixture
def player_games():
    pid = 456
    page_numbers = [1, 2, 3]
    return PlayerGames(pid, page_numbers)


@pytest.fixture
def game_scrapper():
    game = chess.Board()
    game_str = str(game)
    return GameScrapper(game_str)


def test_html(page_games):
    with patch("requests.Session.get") as mock_get:
        mock_response = mock_get.return_value
        mock_response.status_code = 200
        mock_response.content = b"<html><body><table></table></body></html>"

        html = page_games.html

        mock_get.assert_called_once_with(
            f"https://www.chessgames.com/perl/chess.pl?page={page_games.page_number}&pid={page_games.pid}",
            headers={
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.0.0 Safari/537.36"
            },
        )
        assert isinstance(html, BeautifulSoup)


def test_html_no_content(page_games):
    with patch("requests.Session.get") as mock_get:
        mock_response = mock_get.return_value
        mock_response.status_code = 404
        mock_response.content = b""

        html = page_games.html

        mock_get.assert_called_once_with(
            f"https://www.chessgames.com/perl/chess.pl?page={page_games.page_number}&pid={page_games.pid}",
            headers={
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.0.0 Safari/537.36"
            },
        )
        assert html is None


def test_process_games_table(page_games):
    with patch.object(
        page_games,
        "_html",
        new=BeautifulSoup(
            StringIO(
                "<html><body><table><tr><th>Col1</th><th>Col2</th></tr><tr><td>Data1</td><td>Data2</td></tr></table></body></html>"
            ),
            "html.parser",
        ),
    ):
        games_df = page_games.process_games_table()

        expected_columns = ["Col1", "Col2"]
        assert list(games_df.columns) == expected_columns
        assert len(games_df) == 1
        assert games_df.iloc[0].tolist() == ["Data1", "Data2"]


def test_process_games_table_no_data(page_games):
    with patch.object(
        page_games,
        "_html",
        new=BeautifulSoup(
            StringIO(
                "<html><body><table><tr><th>Col1</th><th>Col2</th></tr></table></body></html>"
            ),
            "html.parser",
        ),
    ):
        games_df = page_games.process_games_table()

        expected_columns = ["Col1", "Col2"]
        assert list(games_df.columns) == expected_columns
        assert len(games_df) == 0


def test_extract_games_links(page_games):
    with patch.object(
        page_games,
        "_html",
        new=BeautifulSoup(
            StringIO(
                '<html><body><table><tr><td><a href="game1.html">Game1</a></td><td><a href="game2.html">Game2</a></td></tr></table></body></html>'
            ),
            "html.parser",
        ),
    ):
        games_links = page_games.extract_games_links()

        expected_games_links = ["game1.html", "game2.html"]
        assert games_links == expected_games_links


def test_extract_games_links_no_links(page_games):
    with patch.object(
        page_games,
        "_html",
        new=BeautifulSoup(
            StringIO(
                "<html><body><table><tr><td>No links</td></tr></table></body></html>"
            ),
            "html.parser",
        ),
    ):
        games_links = page_games.extract_games_links()

        assert games_links == []


def test_pid(player_games):
    assert player_games.pid == 456


def test_page_numbers(player_games):
    assert player_games.page_numbers == [1, 2, 3]


def test_get_player_games(player_games):
    with patch("extraction.PageGames.get_games_links") as mock_get_games_links:
        mock_get_games_links.return_value = ["game1.html", "game2.html"]

        games = player_games.get_player_games()

        mock_get_games_links.assert_called_once()
        assert games == ["game1.html", "game2.html"]


def test_game(game_scrapper):
    game = chess.Board()
    assert game_scrapper.game == game


def test_html_game(game_scrapper):
    with patch("requests.Session.get") as mock_get:
        mock_response = mock_get.return_value
        mock_response.status_code = 200
        mock_response.content = (
            b'<html><body><div class="game">Game content</div></body></html>'
        )

        html_game = game_scrapper.html_game

        mock_get.assert_called_once_with(
            f"https://www.chessgames.com/perl/chess.pl?gid={game_scrapper.game.gid()}",
            headers={
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.0.0 Safari/537.36"
            },
        )
        assert html_game == '<div class="game">Game content</div>'


def test_result(game_scrapper):
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
        result = game_scrapper.result()

        assert result == "1. e4 e5 2. Nf3 Nc6 3. Bb5"


def test_game_type(game_scrapper):
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
        game_type = game_scrapper.game_type()

        assert game_type == "chess"
