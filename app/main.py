from app.Point import Point
from app.Game import BattleKnights

if __name__ == '__main__':
    game = BattleKnights(Point(8, 8))
    game.add_knight('R', 'red', (0, 0))
    game.add_knight('B', 'blue', (0, 2))
    game.add_item('magic_staff', (1, 1, 2), (0, 1))
    game.add_item('axe', (2, 0, 3), (0, 1))

    print(game.board_I)
    print(game.board_K)
    print(game.status_json())

    with open("moves.txt") as f:
        for lineno, line in enumerate(f, start=1):
            line = line.strip()
            if line == "GAME-START":
                continue
            if line == "GAME-END":
                break
            game.progress_game(line, lineno)
            print(game.board_I)
            print(game.board_K)
            print(game.status_json())
