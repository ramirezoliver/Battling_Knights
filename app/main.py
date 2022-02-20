from typing import Dict, Any, Tuple
import json
from dataclasses import dataclass, astuple


@dataclass()
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

    def move(self, dir_code: str) -> Point:
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
        elif new_status == 'DEAD':
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
        self.board_K[astuple(knight.position)] = name
        self.K_code_map[code] = name

    def add_item(self, name: str, item_stats: Tuple, yx_tuple: Tuple):
        item = ItemState(Point(*yx_tuple))
        self.status[name] = item
        self.items_map[name] = ItemStats(*item_stats)

        self.add_item_to_board(name, item.position)

    def add_item_to_board(self, name: str, position: Point):
        item_position = astuple(position)
        if item_position in self.board_I:
            self.board_I[item_position].append(name)
        else:
            self.board_I[item_position] = [name]

    def get_highest_priority_item(self, position: Point):
        present_items = self.board_I[astuple(position)]
        item = present_items[0]
        if len(present_items) > 1:
            index_item = 0
            for i in range(1, len(present_items)):
                x = present_items[i]
                if self.items_map[x].priority > self.items_map[item].priority:
                    item = x
                    index_item = i
            self.board_I[astuple(position)].pop(index_item)
        else:
            self.board_I.pop(astuple(position))
        return item

    def acquire_item(self, knight: str):
        item = self.get_highest_priority_item(self.status[knight].position)
        self.status[item].equipped = True
        self.status[knight].equip_item(item, self.items_map[item])

    def drop_item(self, knight: str):
        item = self.status[knight].item
        if item is not None:
            self.status[item].equipped = False
            self.add_item_to_board(item, self.status[item].position)

    def battle(self, attacker: str, defender: str) -> str:
        winner = loser = ''
        position = self.status[defender].position
        if self.status[attacker].attack + .5 > self.status[defender].defense:
            winner, loser = attacker, defender
        else:
            winner, loser = defender, attacker

        self.status[loser].update_status('DEAD')
        self.drop_item(loser)
        self.board_K[astuple(position)] = winner
        return winner

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

        if self.status[knight].status in {'DROWNED', 'DEAD'}:
            return self.status

        self.board_K.pop(astuple(self.status[knight].position))
        new_position = self.status[knight].move(dir_code)
        equipped_item = self.status[knight].item
        board_key = astuple(new_position)

        if not (0 <= self.status[knight].position.x < self.size.x and
                0 <= self.status[knight].position.y < self.size.y):

            self.status[knight].update_status('DROWNED')
            self.drop_item(knight)
            return self.status

        if equipped_item:
            self.status[equipped_item].position = new_position
        elif board_key in self.board_I and equipped_item is None:
            self.acquire_item(knight)

        if board_key in self.board_K:
            opponent = self.board_K[board_key]
            self.battle(knight, opponent)
        else:
            self.board_K[board_key] = knight

        return self.status


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
