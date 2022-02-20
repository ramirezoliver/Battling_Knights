from dataclasses import dataclass
from app.Point import Point


@dataclass
class ItemStats():
    attack: int
    defense: int
    priority: int


@dataclass
class ItemState():
    position: Point
    equipped: bool = False
