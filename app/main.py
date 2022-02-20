from app.Point import Point
from app.Game import BattleKnights

if __name__ == '__main__':
    game = BattleKnights(Point(8, 8))
    game.add_knight('R', 'red', (0, 0))
    game.add_knight('B', 'blue', (7, 0))
    game.add_knight('G', 'green', (7, 7))
    game.add_knight('Y', 'yellow', (0, 7))
    game.add_item('axe', (1, 1, 3), (2, 2))
    game.add_item('dagger', (2, 0, 1), (2, 5))
    game.add_item('magic_staff', (2, 0, 2), (5, 2))
    game.add_item('helmet', (2, 0, 0), (5, 5))

    game.run_moves_from_file('moves.txt')
    with open('final_state.json', 'w') as f:
        f.write(game.status_json())
