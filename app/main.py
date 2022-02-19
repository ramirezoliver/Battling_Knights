from typing import List, Dict, Any
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
    position: Point
    status: str = 'LIVE'
    item: Any = None
    attack: int = 1
    defense: int = 1

@dataclass
class Knight():
    code: str
    name: str
    state: KnightState

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


class BattleKnights():
    DIRECTIONS: Dict = {"N": Point(-1,0), "S": Point(1,0) , "E": Point(0,1) ,"W": Point(0,-1)}
    def __init__(self, size: Point, list_knights: List[Knight], list_items: List[Item]):
        status_knights: Dict = {KN.name: KN.state for KN in list_knights}
        status_items: Dict = {IT.name: IT.state for IT in list_items}

        self.status: Dict = {**status_knights, **status_items}
        self.items_stats: Dict = {IT.name: IT.stats for IT in list_items} #item A/D table
        self.knight_codes: Dict = {KN.code: KN.name for KN in list_knights}
        self.board_knights: Dict = {KN.state.position: KN.name for KN in list_knights} #positions of LIVE Knights
        self.board_free_items: Dict = {IT.state.position: IT.name for IT in list_items} #positions of free Items
        self.size: Point = size

    def progress_game(self, line: str, lineno: int) -> Dict:
        step = line.split(':')
        if len(step) != 2:
            raise Exception(f'Invalid step format in line {lineno}')
        elif step[0] not in self.knight_codes:
            raise Exception(f'Invalid knight code in line {lineno}')
        elif step[1] not in self.DIRECTIONS:
            raise Exception(f'Invalid direction in line {lineno}')
        self.game_step(step[0], step[1])
        return self.status

    def game_step(self, KN_code: str, dir_code: str) -> Dict:
        name = self.knight_codes[KN_code]
        self.status[name].position.move(dir_code)
        return self.status

    def status_json(self):
        status = {k: astuple(v) for k, v in self.status.items()}
        return json.dumps(status)


if __name__ == '__main__':
    game = BattleKnights(
        Point(8,8),
        [
            Knight('R','red',KnightState(Point(1,2))),
            Knight('B','blue',KnightState(Point(1,5)))
        ],
        [
            Item('magic_staff',ItemStats(1,0,0), ItemState(Point(0,0)))
        ]
    )

    with open ("moves.txt") as f:
        for lineno, line in enumerate(f, start= 1):
            line = line.strip()
            if line == "GAME-END":
                break
            elif line == "GAME-START":
                continue                    
            game.progress_game(line,lineno)
            
            print(game.status_json())
            