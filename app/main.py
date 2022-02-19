from typing import Dict, Any, Tuple
import json
from dataclasses import dataclass, astuple


@dataclass(unsafe_hash=True)
class Point():
    y: int
    x: int

    def move(self, dir_code: str):
        if dir_code == 'N':
            self.y += -1
        elif dir_code == 'S':
            self.y += 1
        elif dir_code == 'W':
            self.x += -1
        elif dir_code == 'E':
            self.x += 1


@dataclass
class KnightState():
    position: Any
    status: str = 'LIVE'
    item: Any = None
    attack: int = 1
    defense: int = 1

    def update_status(self, new_status: str) -> None:
        self.status = new_status
        if new_status == 'DROWNED':
            self.position = None
            self.attack = 0
            self.defense = 0


@dataclass
class Knight():
    code: str
    name: str
    state: KnightState

    def __init__(self, code: str, name: str, yx_tuple: Tuple):
        self.code = code
        self.name = name
        self.state = KnightState(Point(*yx_tuple))


@dataclass
class ItemState():
    position: Point
    equipped: bool = False


@dataclass
class ItemStats():
    attack: int
    defense: int
    priority: int


@dataclass
class Item():
    name: str
    stats: ItemStats
    state: ItemState

    def __init__(self, name: str, item_stats: Tuple, yx_tuple: Tuple):
        self.name = name
        self.stats = ItemStats(*item_stats)
        self.state = ItemState(Point(*yx_tuple))


class BattleKnights():
    def __init__(self, size: Point):
        self.status: Dict = {}
        self.size: Point = size

        # positions of LIVE Knights
        self.board_K: Dict = {}
        self.K_code_map: Dict = {}

        # item A/D table
        self.items_stats: Dict = {}
        # positions of free Items
        self.board_I: Dict = {}

    def add_knight(self, knight: Knight):
        self.status[knight.name] = knight.state
        self.board_K[knight.state.position] = knight.name
        self.K_code_map[knight.code] = knight.name

    def add_item(self, item: Item):
        self.status[item.name] = item.state
        self.board_I[item.state.position] = item.name
        self.items_stats[item.name] = item.stats

    def progress_game(self, line: str, lineno: int) -> Dict:
        DIRECTIONS: set = {"N", "S", "W", "E"}
        step = line.split(':')
        if len(step) != 2:
            raise Exception(f'Invalid step format in line {lineno}')
        elif step[0] not in self.K_code_map:
            raise Exception(f'Invalid knight code in line {lineno}')
        elif step[1] not in DIRECTIONS:
            raise Exception(f'Invalid direction in line {lineno}')
        self.game_step(step[0], step[1])
        return self.status

    def status_json(self):
        status = {k: astuple(v) for k, v in self.status.items()}
        return json.dumps(status)

    def game_step(self, KN_code: str, dir_code: str) -> Dict:
        knight = self.K_code_map[KN_code]

        if self.status[knight].status == 'DROWNED':
            return self.status

        self.status[knight].position.move(dir_code)

        if not (0 <= self.status[knight].position.x < self.size.x and
                0 <= self.status[knight].position.y < self.size.y):

            self.status[knight].update_status('DROWNED')

        return self.status


if __name__ == '__main__':
    game = BattleKnights(Point(8, 8))
    game.add_knight(Knight('R', 'red', (0, 1)))
    game.add_knight(Knight('R', 'red', (0, 1)))
    game.add_item(Item('magic_staff', (1, 0, 0), (0, 0)))

    with open("moves.txt") as f:
        for lineno, line in enumerate(f, start=1):
            line = line.strip()
            if line == "GAME-END":
                break
            elif line == "GAME-START":
                continue
            game.progress_game(line, lineno)

            print(game.status_json())
