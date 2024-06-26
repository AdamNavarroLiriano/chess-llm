import pandas as pd
import numpy as np 
import requests
from bs4 import BeautifulSoup

import chess
import chess.pgn
import io


pgn = io.StringIO("""
[Event "Live Chess"]
[Site "Chess.com"]  
[Date "2021.08.05"] 
[Round "-"]
[White "urvishmhjn"]
[Black "yannickhs"]
[Result "1-0"]
[CurrentPosition "r1b1q1r1/p2nbk2/4pp1Q/1p1p3B/2pP3N/1PP1P3/P4PPP/R4RK1 b - -"]
[Timezone "UTC"]
[ECO "A45"]
[UTCDate "2021.08.05"]
[UTCTime "09:25:32"]
[WhiteElo "1220"]
[BlackElo "1140"]
[TimeControl "900+10"]
[Termination "urvishmhjn won by resignation"]

1. d4 Nf6 2. Bf4 e6 3. e3 d5 4. Bd3 c5 5. c3 c4 6. Be2 Nc6 
7. Nf3 Be7 8. Nbd2 O-O 9. O-O Nh5 10. Be5 Nxe5 11. Nxe5 Nf6 
12. b3 b5 13. Qc2 Nd7 14. Ndf3 f6 15. Ng4 h5 16. Nh6+ gxh6 
17. Qg6+ Kh8 18. Qxh6+ Kg8 19. Qxh5 Qe8 20. Qg4+ Kf7 
21. Nh4 Rg8 22. Qh5+ Kf8 23. Qh6+ Kf7 24. Bh5+ 1-0 
                  """)

pgn = io.StringIO("""
1. d4 Nf6 2. Bf4 e6 3. e3 d5 4. Bd3 c5 5. c3 c4 6. Be2 Nc6 
7. Nf3 Be7 8. Nbd2 O-O 9. O-O Nh5 10. Be5 Nxe5 11. Nxe5 Nf6 
12. b3 b5 13. Qc2 Nd7 14. Ndf3 f6 15. Ng4 h5 16. Nh6+ gxh6 
17. Qg6+ Kh8 18. Qxh6+ Kg8 19. Qxh5 Qe8 20. Qg4+ Kf7 
21. Nh4 Rg8 22. Qh5+ Kf8 23. Qh6+ Kf7 24. Bh5+ 0-1
                  """)

game = chess.pgn.read_game(pgn)

game.headers['Result']


chess.Board(game.board().fen()).outcome().result()

while game.next():
    print(game.board().fen())
    game=game.next()

game.san()

game
# LAST MOVE: game.san()

