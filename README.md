# Battling Knights
![pyversion](https://img.shields.io/badge/python-3.8-blue.svg)

## Running Commands

Command line from root directory
```sh
python -m main.app
```

Using `make` and` Makefile`
```sh
make run_moves
```

### Testing
Command line from root directory
```sh
coverage run --source=app -m pytest tests/ut
```

Using `make` and `Makefile`
```sh
make test
```

## Class List

Most of these uses `@dataclass` decorator introduced in python 3.7 (PEP557)
* `Point`: Contains 2D coordinate
* `ItemStats`: Contains item attributes, ie. attack, defense and relative priority
* `ItemState`: Contains item state relative to game being played, ie. position and if equipped
* `Knight`: Contains knight status and attributes. Can do the following:
    + `move`: Manipulate Point coordinate in response to commands
    + `equip_item`: Update attribute upon equipping an item
* `BattlingKnights`:  Contains logic for the game
    + Notable class data
        + `status`: Contains current status of game
        + `cells_knights`: position mapping of LIVE knights on the board
        + `cells_items`: position mapping of free items on the board
