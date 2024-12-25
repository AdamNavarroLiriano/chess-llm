import numpy as np

# given,expected: pgn, (len of moves, array of parsed moves)
test_pgns = [
    (
        "1. e4 1/2-1/2",
        (1, np.array([["e4", ""]])),
    ),
    (
        "1. e4  1/2-1/2",
        (1, np.array([["e4", ""]])),
    ),
    (
        "1.e4 1-0",
        (1, np.array([["e4", ""]])),
    ),
    (
        "1.      e4 1-0",
        (1, np.array([["e4", ""]])),
    ),
    (
        "1. e4  e5 1-0",
        (1, np.array([["e4", "e5"]])),
    ),
    (
        "1. e4 e5 2. d4 1-0",
        (2, np.array([["e4", "e5"], ["d4", ""]])),
    ),
    (
        "1. e4 e5 2. d4 d5 1-0",
        (2, np.array([["e4", "e5"], ["d4", "d5"]])),
    ),
]


# given,expected: (pgn, number of samples),
# [(<BOG> | moves array before white's next moves), white next move)]
test_white_positions = [
    (("1. e4 1-0", 5), [("<BOG>", "e4")]),
    (
        ("1. e4 e5 2. d4 1-0", 5),
        [("<BOG>", "e4"), (np.array([["e4", "e5"]]), "d4")],
    ),
]

test_black_positions = [
    (("1. e4 1-0", 5), [("<BOG>", "e4")]),
    (
        ("1. e4 e5 2. d4 1-0", 5),
        [("<BOG>", "e4"), (np.array([["e4", "e5"]]), "d4")],
    ),
]

test_player_games = [
    {
        "game": "A vs B",
        "result": "1-0",
        "year": 2024,
        "gid": "1",
        "is_white": False,
    },
    {
        "game": "B vs A",
        "result": "1/2-1/2",
        "year": 2024,
        "gid": "2",
        "is_white": True,
    },
]

test_games_dict = [
    {
        "gid": "1",
        "data": {
            "fens": [
                [
                    "rnbqkbnr\\/pppppppp\\/8\\/8\\/3P4\\/8\\/PPP1PPPP\\/RNBQKBNR b KQkq - 0 1",
                    "rnbqkb1r\\/pppppppp\\/5n2\\/8\\/3P4\\/8\\/PPP1PPPP\\/RNBQKBNR w KQkq - 1 2",
                ],
                [
                    "rnbqkb1r\\/pppppppp\\/5n2\\/8\\/2PP4\\/8\\/PP2PPPP\\/RNBQKBNR b KQkq - 0 2",
                    "rnbqkb1r\\/pppp1ppp\\/4pn2\\/8\\/2PP4\\/8\\/PP2PPPP\\/RNBQKBNR w KQkq - 0 3",
                ],
                [
                    "rnbqkb1r\\/pppp1ppp\\/4pn2\\/8\\/2PP4\\/2N5\\/PP2PPPP\\/R1BQKBNR b KQkq - 1 3",
                    "rnbqkb1r\\/ppp2ppp\\/4pn2\\/3p4\\/2PP4\\/2N5\\/PP2PPPP\\/R1BQKBNR w KQkq - 0 4",
                ],
                [
                    "rnbqkb1r\\/ppp2ppp\\/4pn2\\/3P4\\/3P4\\/2N5\\/PP2PPPP\\/R1BQKBNR b KQkq - 0 4",
                    "rnbqkb1r\\/ppp2ppp\\/5n2\\/3p4\\/3P4\\/2N5\\/PP2PPPP\\/R1BQKBNR w KQkq - 0 5",
                ],
                [
                    "rnbqkb1r\\/ppp2ppp\\/5n2\\/3p2B1\\/3P4\\/2N5\\/PP2PPPP\\/R2QKBNR b KQkq - 1 5",
                    "rnbqk2r\\/ppp1bppp\\/5n2\\/3p2B1\\/3P4\\/2N5\\/PP2PPPP\\/R2QKBNR w KQkq - 2 6",
                ],
                [
                    "rnbqk2r\\/ppp1bppp\\/5n2\\/3p2B1\\/3P4\\/2N1P3\\/PP3PPP\\/R2QKBNR b KQkq - 0 6",
                    "rnbqk2r\\/ppp1bpp1\\/5n1p\\/3p2B1\\/3P4\\/2N1P3\\/PP3PPP\\/R2QKBNR w KQkq - 0 7",
                ],
                [
                    "rnbqk2r\\/ppp1bpp1\\/5n1p\\/3p4\\/3P3B\\/2N1P3\\/PP3PPP\\/R2QKBNR b KQkq - 1 7",
                    "rn1qk2r\\/ppp1bpp1\\/5n1p\\/3p4\\/3P2bB\\/2N1P3\\/PP3PPP\\/R2QKBNR w KQkq - 2 8",
                ],
                [
                    "rn1qk2r\\/ppp1bpp1\\/5n1p\\/3p4\\/3P2bB\\/2N1PP2\\/PP4PP\\/R2QKBNR b KQkq - 0 8",
                    "rn1qk2r\\/ppp1bpp1\\/4bn1p\\/3p4\\/3P3B\\/2N1PP2\\/PP4PP\\/R2QKBNR w KQkq - 1 9",
                ],
                [
                    "rn1qk2r\\/ppp1bpp1\\/4bn1p\\/3p4\\/3P3B\\/2NBPP2\\/PP4PP\\/R2QK1NR b KQkq - 2 9",
                    "rn1qk2r\\/pp2bpp1\\/4bn1p\\/2pp4\\/3P3B\\/2NBPP2\\/PP4PP\\/R2QK1NR w KQkq - 0 10",
                ],
                [
                    "rn1qk2r\\/pp2bpp1\\/4bn1p\\/2pp4\\/3P3B\\/2NBPP2\\/PP2N1PP\\/R2QK2R b KQkq - 1 10",
                    "r2qk2r\\/pp2bpp1\\/2n1bn1p\\/2pp4\\/3P3B\\/2NBPP2\\/PP2N1PP\\/R2QK2R w KQkq - 2 11",
                ],
                [
                    "r2qk2r\\/pp2bpp1\\/2n1bn1p\\/2pp4\\/3P3B\\/2NBPP2\\/PP2N1PP\\/R2Q1RK1 b kq - 3 11",
                    "r2q1rk1\\/pp2bpp1\\/2n1bn1p\\/2pp4\\/3P3B\\/2NBPP2\\/PP2N1PP\\/R2Q1RK1 w - - 4 12",
                ],
                [
                    "r2q1rk1\\/pp2bpp1\\/2n1bn1p\\/2pp4\\/3P3B\\/2NBPP2\\/PP2N1PP\\/R2QR1K1 b - - 5 12",
                    "r2qr1k1\\/pp2bpp1\\/2n1bn1p\\/2pp4\\/3P3B\\/2NBPP2\\/PP2N1PP\\/R2QR1K1 w - - 6 13",
                ],
                [
                    "r2qr1k1\\/pp2bpp1\\/2n1bn1p\\/2pp4\\/3P3B\\/2N1PP2\\/PPB1N1PP\\/R2QR1K1 b - - 7 13",
                    "2rqr1k1\\/pp2bpp1\\/2n1bn1p\\/2pp4\\/3P3B\\/2N1PP2\\/PPB1N1PP\\/R2QR1K1 w - - 8 14",
                ],
                [
                    "2rqr1k1\\/pp2bpp1\\/2n1bn1p\\/2pp4\\/3P1N1B\\/2N1PP2\\/PPB3PP\\/R2QR1K1 b - - 9 14",
                    "2rqr1k1\\/pp2bpp1\\/2n1bn1p\\/3p4\\/3p1N1B\\/2N1PP2\\/PPB3PP\\/R2QR1K1 w - - 0 15",
                ],
                [
                    "2rqr1k1\\/pp2bpp1\\/2n1Nn1p\\/3p4\\/3p3B\\/2N1PP2\\/PPB3PP\\/R2QR1K1 b - - 0 15",
                    "2rqr1k1\\/pp2b1p1\\/2n1pn1p\\/3p4\\/3p3B\\/2N1PP2\\/PPB3PP\\/R2QR1K1 w - - 0 16",
                ],
                [
                    "2rqr1k1\\/pp2b1p1\\/2n1pn1p\\/3p4\\/3P3B\\/2N2P2\\/PPB3PP\\/R2QR1K1 b - - 0 16",
                    "2rqr1k1\\/pp2b1p1\\/4pn1p\\/3p4\\/3n3B\\/2N2P2\\/PPB3PP\\/R2QR1K1 w - - 0 17",
                ],
                [
                    "2rqr1k1\\/pp2b1p1\\/4pnBp\\/3p4\\/3n3B\\/2N2P2\\/PP4PP\\/R2QR1K1 b - - 1 17",
                    "2rq1rk1\\/pp2b1p1\\/4pnBp\\/3p4\\/3n3B\\/2N2P2\\/PP4PP\\/R2QR1K1 w - - 2 18",
                ],
                [
                    "2rq1rk1\\/pp2b1p1\\/4pnBp\\/3p4\\/3n4\\/2N2P2\\/PP3BPP\\/R2QR1K1 b - - 3 18",
                    "2rq1rk1\\/pp2b1p1\\/2n1pnBp\\/3p4\\/8\\/2N2P2\\/PP3BPP\\/R2QR1K1 w - - 4 19",
                ],
                [
                    "2rq1rk1\\/pp2b1p1\\/2n1RnBp\\/3p4\\/8\\/2N2P2\\/PP3BPP\\/R2Q2K1 b - - 0 19",
                    "2rq1rk1\\/pp2b1p1\\/2n1RnBp\\/8\\/3p4\\/2N2P2\\/PP3BPP\\/R2Q2K1 w - - 0 20",
                ],
                [
                    "2rq1rk1\\/pp2b1p1\\/2n1RnBp\\/8\\/3p4\\/5P2\\/PP2NBPP\\/R2Q2K1 b - - 1 20",
                    "2rq1rk1\\/pp4p1\\/2n1RnBp\\/2b5\\/3p4\\/5P2\\/PP2NBPP\\/R2Q2K1 w - - 2 21",
                ],
                [
                    "2rq1rk1\\/pp4p1\\/2n1RnBp\\/2b5\\/3p1N2\\/5P2\\/PP3BPP\\/R2Q2K1 b - - 3 21",
                    "2rq1rk1\\/pp4p1\\/2n1R1Bp\\/2bn4\\/3p1N2\\/5P2\\/PP3BPP\\/R2Q2K1 w - - 4 22",
                ],
                [
                    "2rq1rk1\\/pp4p1\\/2n1R1Bp\\/2bn4\\/3p1N2\\/1Q3P2\\/PP3BPP\\/R5K1 b - - 5 22",
                    "2rq1rk1\\/pp4p1\\/2n1R1Bp\\/2b5\\/3p1n2\\/1Q3P2\\/PP3BPP\\/R5K1 w - - 0 23",
                ],
                [
                    "2rq1rk1\\/pp4p1\\/2nR2Bp\\/2b5\\/3p1n2\\/1Q3P2\\/PP3BPP\\/R5K1 b - - 1 23",
                    "2rq1r1k\\/pp4p1\\/2nR2Bp\\/2b5\\/3p1n2\\/1Q3P2\\/PP3BPP\\/R5K1 w - - 2 24",
                ],
                [
                    "2rR1r1k\\/pp4p1\\/2n3Bp\\/2b5\\/3p1n2\\/1Q3P2\\/PP3BPP\\/R5K1 b - - 0 24",
                    "3r1r1k\\/pp4p1\\/2n3Bp\\/2b5\\/3p1n2\\/1Q3P2\\/PP3BPP\\/R5K1 w - - 0 25",
                ],
                [
                    "3r1r1k\\/pQ4p1\\/2n3Bp\\/2b5\\/3p1n2\\/5P2\\/PP3BPP\\/R5K1 b - - 0 25",
                    "3r1r1k\\/pQ4p1\\/6Bp\\/2b1n3\\/3p1n2\\/5P2\\/PP3BPP\\/R5K1 w - - 1 26",
                ],
                [
                    "3r1r1k\\/pQ4p1\\/7p\\/2b1n3\\/3pBn2\\/5P2\\/PP3BPP\\/R5K1 b - - 2 26",
                    "3r1r1k\\/pQ4p1\\/1b5p\\/4n3\\/3pBn2\\/5P2\\/PP3BPP\\/R5K1 w - - 3 27",
                ],
                [
                    "3r1r1k\\/pQ4p1\\/1b5p\\/4n3\\/P2pBn2\\/5P2\\/1P3BPP\\/R5K1 b - - 0 27",
                    "3r1r1k\\/pQ4p1\\/1b5p\\/8\\/P1npBn2\\/5P2\\/1P3BPP\\/R5K1 w - - 1 28",
                ],
                [
                    "3r1r1k\\/p5p1\\/Qb5p\\/8\\/P1npBn2\\/5P2\\/1P3BPP\\/R5K1 b - - 2 28",
                    "3r1r1k\\/p5p1\\/Qb5p\\/8\\/P2pBn2\\/5P2\\/1P1n1BPP\\/R5K1 w - - 3 29",
                ],
                [
                    "3r1r1k\\/p5p1\\/Qb5p\\/P7\\/3pBn2\\/5P2\\/1P1n1BPP\\/R5K1 b - - 0 29",
                    "3r1r1k\\/p5p1\\/Q6p\\/P1b5\\/3pBn2\\/5P2\\/1P1n1BPP\\/R5K1 w - - 1 30",
                ],
                [
                    "3r1r1k\\/pB4p1\\/Q6p\\/P1b5\\/3p1n2\\/5P2\\/1P1n1BPP\\/R5K1 b - - 2 30",
                    "3r1r1k\\/pB4p1\\/Q6p\\/P1b5\\/3p1n2\\/1n3P2\\/1P3BPP\\/R5K1 w - - 3 31",
                ],
                [
                    "3r1r1k\\/pB4p1\\/Q6p\\/P1b5\\/3p1n2\\/1n3P2\\/1P3BPP\\/3R2K1 b - - 4 31",
                    "3r1r1k\\/pB4p1\\/Q6p\\/P1b5\\/5n2\\/1n1p1P2\\/1P3BPP\\/3R2K1 w - - 0 32",
                ],
                [
                    "3r1r1k\\/pB4p1\\/Q6p\\/P1B5\\/5n2\\/1n1p1P2\\/1P4PP\\/3R2K1 b - - 0 32",
                    "3r1r1k\\/pB4p1\\/Q6p\\/P1n5\\/5n2\\/3p1P2\\/1P4PP\\/3R2K1 w - - 0 33",
                ],
                [
                    "3r1r1k\\/QB4p1\\/7p\\/P1n5\\/5n2\\/3p1P2\\/1P4PP\\/3R2K1 b - - 0 33",
                    "3r1r1k\\/Qn4p1\\/7p\\/P7\\/5n2\\/3p1P2\\/1P4PP\\/3R2K1 w - - 0 34",
                ],
                [
                    "3r1r1k\\/1Q4p1\\/7p\\/P7\\/5n2\\/3p1P2\\/1P4PP\\/3R2K1 b - - 0 34",
                    "3rr2k\\/1Q4p1\\/7p\\/P7\\/5n2\\/3p1P2\\/1P4PP\\/3R2K1 w - - 1 35",
                ],
                [
                    "3rr2k\\/1Q4p1\\/7p\\/P7\\/5n2\\/3p1PP1\\/1P5P\\/3R2K1 b - - 0 35",
                    "3rr2k\\/1Q4p1\\/7p\\/P7\\/5n2\\/5PP1\\/1P1p3P\\/3R2K1 w - - 0 36",
                ],
                [
                    "3rr2k\\/6p1\\/7p\\/P7\\/1Q3n2\\/5PP1\\/1P1p3P\\/3R2K1 b - - 1 36",
                    "4r2k\\/6p1\\/7p\\/P7\\/1Q1r1n2\\/5PP1\\/1P1p3P\\/3R2K1 w - - 2 37",
                ],
                [
                    "4r2k\\/6p1\\/7p\\/P7\\/3r1n2\\/5PP1\\/1P1Q3P\\/3R2K1 b - - 0 37",
                    "4r2k\\/6p1\\/7p\\/P7\\/5n2\\/5PP1\\/1P1r3P\\/3R2K1 w - - 0 38",
                ],
                [
                    "4r2k\\/6p1\\/7p\\/P7\\/5n2\\/5PP1\\/1P1R3P\\/6K1 b - - 0 38",
                    "4r2k\\/6p1\\/4n2p\\/P7\\/8\\/5PP1\\/1P1R3P\\/6K1 w - - 1 39",
                ],
                [
                    "4r2k\\/6p1\\/4n2p\\/P7\\/1P6\\/5PP1\\/3R3P\\/6K1 b - - 0 39",
                    "4r1k1\\/6p1\\/4n2p\\/P7\\/1P6\\/5PP1\\/3R3P\\/6K1 w - - 1 40",
                ],
                [
                    "4r1k1\\/6p1\\/4n2p\\/PP6\\/8\\/5PP1\\/3R3P\\/6K1 b - - 0 40",
                    "r5k1\\/6p1\\/4n2p\\/PP6\\/8\\/5PP1\\/3R3P\\/6K1 w - - 1 41",
                ],
                [
                    "r5k1\\/6p1\\/4n2p\\/PP6\\/8\\/5PP1\\/R6P\\/6K1 b - - 2 41",
                    "r7\\/5kp1\\/4n2p\\/PP6\\/8\\/5PP1\\/R6P\\/6K1 w - - 3 42",
                ],
                [
                    "r7\\/5kp1\\/4n2p\\/PP6\\/8\\/5PP1\\/R4K1P\\/8 b - - 4 42",
                    "r7\\/4k1p1\\/4n2p\\/PP6\\/8\\/5PP1\\/R4K1P\\/8 w - - 5 43",
                ],
                [
                    "r7\\/4k1p1\\/1P2n2p\\/P7\\/8\\/5PP1\\/R4K1P\\/8 b - - 0 43",
                    "r7\\/4k1p1\\/1P5p\\/P1n5\\/8\\/5PP1\\/R4K1P\\/8 w - - 1 44",
                ],
                [
                    "r7\\/4k1p1\\/1P5p\\/P1n5\\/8\\/4KPP1\\/R6P\\/8 b - - 2 44",
                    "r7\\/6p1\\/1P1k3p\\/P1n5\\/8\\/4KPP1\\/R6P\\/8 w - - 3 45",
                ],
                [
                    "r7\\/6p1\\/1P1k3p\\/P1n5\\/5K2\\/5PP1\\/R6P\\/8 b - - 4 45",
                    "r7\\/8\\/1P1k2pp\\/P1n5\\/5K2\\/5PP1\\/R6P\\/8 w - - 0 46",
                ],
                [
                    "r7\\/8\\/1P1k2pp\\/P1n5\\/5K1P\\/5PP1\\/R7\\/8 b - - 0 46",
                    "r7\\/8\\/1P4pp\\/P1nk4\\/5K1P\\/5PP1\\/R7\\/8 w - - 1 47",
                ],
                [
                    "r7\\/8\\/1P4pp\\/P1nk4\\/6KP\\/5PP1\\/R7\\/8 b - - 2 47",
                    "r7\\/8\\/1Pk3pp\\/P1n5\\/6KP\\/5PP1\\/R7\\/8 w - - 3 48",
                ],
                [
                    "r7\\/8\\/1Pk3pp\\/P1n4P\\/6K1\\/5PP1\\/R7\\/8 b - - 0 48",
                    "6r1\\/8\\/1Pk3pp\\/P1n4P\\/6K1\\/5PP1\\/R7\\/8 w - - 1 49",
                ],
                [
                    "6r1\\/8\\/1Pk3pp\\/P1n4P\\/6K1\\/5PP1\\/2R5\\/8 b - - 2 49",
                    "6r1\\/8\\/1P4pp\\/Pkn4P\\/6K1\\/5PP1\\/2R5\\/8 w - - 3 50",
                ],
                [
                    "6r1\\/8\\/1P4Pp\\/Pkn5\\/6K1\\/5PP1\\/2R5\\/8 b - - 0 50",
                    "8\\/8\\/1P4rp\\/Pkn5\\/6K1\\/5PP1\\/2R5\\/8 w - - 0 51",
                ],
            ],
            "game_type": None,
            "pgn": "1. d4 Nf6 2. c4 e6 3. Nc3 d5 4. cxd5 exd5 5. Bg5 Be7 6. e3 h6 7. Bh4 Bg4 8. f3\\nBe6 9. Bd3 c5 10. Nge2 Nc6 11. O-O O-O 12. Re1 Re8 13. Bc2 Rc8 14. Nf4 cxd4 15.\\nNxe6 fxe6 16. exd4 Nxd4 17. Bg6 Rf8 18. Bf2 Nc6 19. Rxe6 d4 20. Ne2 Bc5 21. Nf4\\nNd5 22. Qb3 Nxf4 23. Rd6+ Kh8 24. Rxd8 Rcxd8 25. Qxb7 Ne5 26. Be4 Bb6 27. a4\\nNc4 28. Qa6 Nd2 29. a5 Bc5 30. Bb7 Nb3 31. Rd1 d3 32. Bxc5 Nxc5 33. Qxa7 Nxb7\\n34. Qxb7 Rfe8 35. g3 d2 36. Qb4 Rd4 37. Qxd2 Rxd2 38. Rxd2 Ne6 39. b4 Kg8 40.\\nb5 Ra8 41. Ra2 Kf7 42. Kf2 Ke7 43. b6 Nc5 44. Ke3 Kd6 45. Kf4 g6 46. h4 Kd5 47.\\nKg4 Kc6 48. h5 Rg8 49. Rc2 Kb5 50. hxg6 Rxg6+ 51. Kh5 1-0",
            "result": "1-0",
        },
    },
    {
        "gid": "2",
        "data": {
            "fens": [
                [
                    "rnbqkbnr\\/pppppppp\\/8\\/8\\/3P4\\/8\\/PPP1PPPP\\/RNBQKBNR b KQkq - 0 1",
                    "rnbqkb1r\\/pppppppp\\/5n2\\/8\\/3P4\\/8\\/PPP1PPPP\\/RNBQKBNR w KQkq - 1 2",
                ],
                [
                    "rnbqkb1r\\/pppppppp\\/5n2\\/8\\/2PP4\\/8\\/PP2PPPP\\/RNBQKBNR b KQkq - 0 2",
                    "rnbqkb1r\\/pppp1ppp\\/4pn2\\/8\\/2PP4\\/8\\/PP2PPPP\\/RNBQKBNR w KQkq - 0 3",
                ],
                [
                    "rnbqkb1r\\/pppp1ppp\\/4pn2\\/8\\/2PP4\\/2N5\\/PP2PPPP\\/R1BQKBNR b KQkq - 1 3",
                    "rnbqk2r\\/pppp1ppp\\/4pn2\\/8\\/1bPP4\\/2N5\\/PP2PPPP\\/R1BQKBNR w KQkq - 2 4",
                ],
                [
                    "rnbqk2r\\/pppp1ppp\\/4pn2\\/8\\/1bPP4\\/2N2P2\\/PP2P1PP\\/R1BQKBNR b KQkq - 0 4",
                    "rnbqk2r\\/ppp2ppp\\/4pn2\\/3p4\\/1bPP4\\/2N2P2\\/PP2P1PP\\/R1BQKBNR w KQkq - 0 5",
                ],
                [
                    "rnbqk2r\\/ppp2ppp\\/4pn2\\/3p4\\/1bPP4\\/P1N2P2\\/1P2P1PP\\/R1BQKBNR b KQkq - 0 5",
                    "rnbqk2r\\/ppp2ppp\\/4pn2\\/3p4\\/2PP4\\/P1b2P2\\/1P2P1PP\\/R1BQKBNR w KQkq - 0 6",
                ],
                [
                    "rnbqk2r\\/ppp2ppp\\/4pn2\\/3p4\\/2PP4\\/P1P2P2\\/4P1PP\\/R1BQKBNR b KQkq - 0 6",
                    "rnbqk2r\\/pp3ppp\\/4pn2\\/2pp4\\/2PP4\\/P1P2P2\\/4P1PP\\/R1BQKBNR w KQkq - 0 7",
                ],
                [
                    "rnbqk2r\\/pp3ppp\\/4pn2\\/2pP4\\/3P4\\/P1P2P2\\/4P1PP\\/R1BQKBNR b KQkq - 0 7",
                    "rnbqk2r\\/pp3ppp\\/4p3\\/2pn4\\/3P4\\/P1P2P2\\/4P1PP\\/R1BQKBNR w KQkq - 0 8",
                ],
                [
                    "rnbqk2r\\/pp3ppp\\/4p3\\/2Pn4\\/8\\/P1P2P2\\/4P1PP\\/R1BQKBNR b KQkq - 0 8",
                    "rnb1k2r\\/pp3ppp\\/4p3\\/q1Pn4\\/8\\/P1P2P2\\/4P1PP\\/R1BQKBNR w KQkq - 1 9",
                ],
                [
                    "rnb1k2r\\/pp3ppp\\/4p3\\/q1Pn4\\/4P3\\/P1P2P2\\/6PP\\/R1BQKBNR b KQkq - 0 9",
                    "rnb1k2r\\/pp2nppp\\/4p3\\/q1P5\\/4P3\\/P1P2P2\\/6PP\\/R1BQKBNR w KQkq - 1 10",
                ],
                [
                    "rnb1k2r\\/pp2nppp\\/4p3\\/q1P5\\/4P3\\/P1P1BP2\\/6PP\\/R2QKBNR b KQkq - 2 10",
                    "rnb2rk1\\/pp2nppp\\/4p3\\/q1P5\\/4P3\\/P1P1BP2\\/6PP\\/R2QKBNR w KQ - 3 11",
                ],
                [
                    "rnb2rk1\\/pp2nppp\\/4p3\\/q1P5\\/4P3\\/P1P1BP2\\/3Q2PP\\/R3KBNR b KQ - 4 11",
                    "rnbr2k1\\/pp2nppp\\/4p3\\/q1P5\\/4P3\\/P1P1BP2\\/3Q2PP\\/R3KBNR w KQ - 5 12",
                ],
                [
                    "rnbr2k1\\/pp2nppp\\/4p3\\/q1P5\\/4P3\\/P1P1BP2\\/1Q4PP\\/R3KBNR b KQ - 6 12",
                    "r1br2k1\\/pp2nppp\\/n3p3\\/q1P5\\/4P3\\/P1P1BP2\\/1Q4PP\\/R3KBNR w KQ - 7 13",
                ],
                [
                    "r1br2k1\\/pp2nppp\\/n3p3\\/q1P5\\/4P3\\/P1P1BP1N\\/1Q4PP\\/R3KB1R b KQ - 8 13",
                    "r1br2k1\\/pp2nppp\\/n7\\/q1P1p3\\/4P3\\/P1P1BP1N\\/1Q4PP\\/R3KB1R w KQ - 0 14",
                ],
                [
                    "r1br2k1\\/pp2nppp\\/n7\\/q1P1p3\\/4P3\\/P1P1BP2\\/1Q3NPP\\/R3KB1R b KQ - 1 14",
                    "r2r2k1\\/pp2nppp\\/n3b3\\/q1P1p3\\/4P3\\/P1P1BP2\\/1Q3NPP\\/R3KB1R w KQ - 2 15",
                ],
                [
                    "r2r2k1\\/pp2nppp\\/n3b3\\/q1P1p3\\/4P3\\/P1PNBP2\\/1Q4PP\\/R3KB1R b KQ - 3 15",
                    "r2r2k1\\/ppq1nppp\\/n3b3\\/2P1p3\\/4P3\\/P1PNBP2\\/1Q4PP\\/R3KB1R w KQ - 4 16",
                ],
                [
                    "r2r2k1\\/ppq1nppp\\/n3b3\\/1QP1p3\\/4P3\\/P1PNBP2\\/6PP\\/R3KB1R b KQ - 5 16",
                    "r2r2k1\\/ppqbnppp\\/n7\\/1QP1p3\\/4P3\\/P1PNBP2\\/6PP\\/R3KB1R w KQ - 6 17",
                ],
                [
                    "r2r2k1\\/ppqbnppp\\/n7\\/2P1p3\\/4P3\\/P1PNBP2\\/1Q4PP\\/R3KB1R b KQ - 7 17",
                    "r2r2k1\\/ppq1nppp\\/n3b3\\/2P1p3\\/4P3\\/P1PNBP2\\/1Q4PP\\/R3KB1R w KQ - 8 18",
                ],
                [
                    "r2r2k1\\/ppq1nppp\\/n3b3\\/1QP1p3\\/4P3\\/P1PNBP2\\/6PP\\/R3KB1R b KQ - 9 18",
                    "r2r2k1\\/ppqbnppp\\/n7\\/1QP1p3\\/4P3\\/P1PNBP2\\/6PP\\/R3KB1R w KQ - 10 19",
                ],
                [
                    "r2r2k1\\/ppqbnppp\\/n7\\/2P1p3\\/4P3\\/P1PNBP2\\/1Q4PP\\/R3KB1R b KQ - 11 19",
                    "r2r2k1\\/ppq1nppp\\/n3b3\\/2P1p3\\/4P3\\/P1PNBP2\\/1Q4PP\\/R3KB1R w KQ - 12 20",
                ],
            ],
            "game_type": None,
            "pgn": "1. d4 Nf6 2. c4 e6 3. Nc3 Bb4 4. f3 d5 5. a3 Bxc3+ 6. bxc3 c5 7. cxd5 Nxd5 8.\\ndxc5 Qa5 9. e4 Ne7 10. Be3 O-O 11. Qd2 Rd8 12. Qb2 Na6 13. Nh3 e5 14. Nf2 Be6\\n15. Nd3 Qc7 16. Qb5 Bd7 17. Qb2 Be6 18. Qb5 Bd7 19. Qb2 Be6 20. Qb5 1\\/2-1\\/2",
            "result": "1\\/2-1\\/2",
        },
    },
]
