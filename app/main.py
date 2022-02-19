from typing import Dict, Any, Tuple
import json
from dataclasses import dataclass, astuple


@dataclass(unsafe_hash=True)
class Point():
    y: int
    x: int


@dataclass
class ItemStats():
    attack: int
    defense: int
    priority: int


@dataclass
class ItemState():
    position: Point
    equipped: bool = False


@dataclass
class Knight():
    position: Any
    status: str = 'LIVE'
    item: Any = None
    attack: int = 1
    defense: int = 1

    def move(self, dir_code: str):
        if dir_code == 'N':
            self.position.y += -1
        elif dir_code == 'S':
            self.position.y += 1
        elif dir_code == 'W':
            self.position.x += -1
        elif dir_code == 'E':
            self.position.x += 1
        return self.position

    def update_status(self, new_status: str) -> None:
        self.status = new_status
        if new_status == 'DROWNED':
            self.position = None
            self.attack = 0
            self.defense = 0

    def equip_item(self, item: str, item_stats: ItemStats) -> None:
        self.item = item
        self.attack += item_stats.attack
        self.defense += item_stats.defense


class BattleKnights():
    def __init__(self, size: Point):
        self.status: Dict = {}
        self.size: Point = size

        # positions of LIVE Knights
        self.board_K: Dict = {}
        self.K_code_map: Dict = {}

        # item A/D table
        self.items_map: Dict = {}
        # positions of free Items
        self.board_I: Dict = {}

    def add_knight(self, code: str, name: str, yx_tuple: Tuple):
        knight = Knight(Point(*yx_tuple))
        self.status[name] = knight
        self.board_K[knight.position] = name
        self.K_code_map[code] = name

    def add_item(self, name: str, item_stats: Tuple, yx_tuple: Tuple):
        item = ItemState(Point(*yx_tuple))
        self.status[name] = item
        self.items_map[name] = ItemStats(*item_stats)

        if item.position in self.board_I:
            self.board_I[item.position].append(name)
        else:
            self.board_I[item.position] = [name]

    def get_highest_priority_item(self, position: Point):
        item = self.board_I[position][0]
        index_item = 0
        for i in range(1, len(self.board_I[position])):
            x = self.board_I[position][i]
            if self.items_map[x].priority > self.items_map[item].priority:
                item = x
                index_item = i
        return self.board_I[position].pop(index_item)

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

        equipped_item = self.status[knight].item
        new_position = self.status[knight].move(dir_code)

        if not (0 <= self.status[knight].position.x < self.size.x and
                0 <= self.status[knight].position.y < self.size.y):

            self.status[knight].update_status('DROWNED')
            if equipped_item:
                self.status[equipped_item].equipped = False
            return self.status

        if equipped_item:
            self.status[equipped_item].position = new_position
        elif new_position in self.board_I and equipped_item is None:
            item = self.get_highest_priority_item(new_position)
            item_stats = self.items_map[item]
            self.status[item].equipped = True
            self.status[knight].equip_item(item, item_stats)

        return self.status


if __name__ == '__main__':
    game = BattleKnights(Point(8, 8))
    game.add_knight('R', 'red', (0, 0))
    game.add_item('magic_staff', (1, 1, 2), (0, 1))
    game.add_item('axe', (2, 0, 3), (0, 1))

    with open("moves.txt") as f:
        for lineno, line in enumerate(f, start=1):
            line = line.strip()
            if line == "GAME-END":
                break
            elif line == "GAME-START":
                continue
            game.progress_game(line, lineno)
            print(game.board_I)
            print(game.status_json())
