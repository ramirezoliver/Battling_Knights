from dataclasses import dataclass
from typing import Any
from app.Item import ItemStats
from app.Point import Point


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
