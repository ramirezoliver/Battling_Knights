from app.Knight import Knight
from app.Point import Point
from app.Item import ItemStats


def test_movement_knight():
    knight = Knight(Point(0, 0))

    # perform a loop
    knight.move('S')
    assert knight.position == Point(1, 0)

    knight.move('E')
    assert knight.position == Point(1, 1)

    knight.move('N')
    assert knight.position == Point(0, 1)

    knight.move('W')
    assert knight.position == Point(0, 0)


def test_equip_item():
    knight = Knight(Point(0, 0))

    base_attack = knight.attack
    base_defense = knight.attack

    item_attack = 2
    item_defense = 3
    item_stats = ItemStats(item_attack, item_defense, 3)

    knight.equip_item('fake_name', item_stats)

    assert knight.item == 'fake_name'
    assert knight.attack == item_attack + base_attack
    assert knight.defense == item_defense + base_defense


def test_update_status_dead():
    knight = Knight(Point(0, 0))

    assert knight.status == 'LIVE'

    knight.update_status('DEAD')
    assert knight.position == Point(0, 0)
    assert knight.attack == 0
    assert knight.defense == 0


def test_update_status_drowned():
    knight = Knight(Point(0, 0))

    assert knight.status == 'LIVE'

    knight.update_status('DROWNED')
    assert knight.position is None
    assert knight.attack == 0
    assert knight.defense == 0
