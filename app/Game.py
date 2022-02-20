from typing import Dict, Tuple
import json
from dataclasses import astuple
from app.Point import Point
from app.Knight import Knight
from app.Item import ItemState, ItemStats


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
