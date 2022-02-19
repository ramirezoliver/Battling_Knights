from app.main import BattleKnights, Point


def test_knight_move():
    test_game = BattleKnights(Point(2, 2))
    test_game.add_knight('R', 'red', (0, 0))

    assert test_game.status['red'].position == Point(0, 0)

    # perform a loop
    status = test_game.game_step('R', 'S')
    assert status['red'].position == Point(1, 0)

    status = test_game.game_step('R', 'E')
    assert status['red'].position == Point(1, 1)

    status = test_game.game_step('R', 'N')
    assert status['red'].position == Point(0, 1)

    status = test_game.game_step('R', 'W')
    assert status['red'].position == Point(0, 0)


def test_equip_item():
    test_game = BattleKnights(Point(2, 2))
    test_game.add_knight('R', 'red', (0, 0))
    test_game.add_item('magic_staff', (1, 1, 2), (0, 1))

    status = test_game.game_step('R', 'E')
    assert status['magic_staff'].equipped is True
    assert status['red'].item == 'magic_staff'
    assert status['red'].attack == 2
    assert status['red'].defense == 2

    # ignore a second item
    test_game.add_item('axe', (2, 0, 3), (1, 1))
    status = test_game.game_step('R', 'S')
    assert status['red'].item == 'magic_staff'
    assert status['magic_staff'].equipped is True
    assert status['magic_staff'].position == Point(1, 1)
    assert status['axe'].equipped is False


def test_equip_item_select_higher_priority():
    test_game = BattleKnights(Point(2, 2))
    test_game.add_knight('R', 'red', (0, 0))
    test_game.add_item('magic_staff', (1, 1, 2), (0, 1))
    test_game.add_item('axe', (2, 0, 3), (0, 1))

    status = test_game.game_step('R', 'E')
    assert status['red'].item == 'axe'
    assert status['magic_staff'].equipped is False
    assert status['axe'].equipped is True


def test_drown_knight():
    test_game = BattleKnights(Point(2, 2))
    test_game.add_knight('R', 'red', (0, 0))
    test_game.add_knight('B', 'blue', (1, 1))

    status = test_game.game_step('R', 'N')
    assert status['red'].position is None
    assert status['red'].status == 'DROWNED'
    assert status['red'].attack == 0
    assert status['red'].defense == 0

    status = test_game.game_step('B', 'S')
    assert status['blue'].position is None
    assert status['blue'].status == 'DROWNED'
    assert status['blue'].attack == 0
    assert status['blue'].defense == 0


def test_drown_ignore_further_moves():
    test_game = BattleKnights(Point(2, 2))
    test_game.add_knight('R', 'red', (0, 0))

    status = test_game.game_step('R', 'N')
    assert status['red'].status == 'DROWNED'

    status = test_game.game_step('R', 'S')
    assert status['red'].status == 'DROWNED'


def test_drown_drop_item():
    test_game = BattleKnights(Point(2, 2))
    test_game.add_knight('R', 'red', (0, 0))
    test_game.add_item('magic_staff', (1, 1, 2), (0, 1))

    status = test_game.game_step('R', 'E')
    assert status['magic_staff'].equipped is True
    assert status['red'].item == 'magic_staff'

    status = test_game.game_step('R', 'N')
    assert status['magic_staff'].equipped is False
    assert status['magic_staff'].position == Point(0, 1)
    assert status['red'].status == 'DROWNED'
