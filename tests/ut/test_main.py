from app.main import BattleKnights, Knight, KnightState, Point


def test_movement():
    test_game = BattleKnights(
        Point(2, 2),
        [Knight('R', 'red', KnightState(Point(0, 0)))],
        []
    )

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


def test_drown():
    test_game = BattleKnights(
        size=Point(2, 2),
        knights=[Knight('R', 'red', KnightState(Point(0, 0))),
                 Knight('B', 'blue', KnightState(Point(1, 1)))],
        items=[]
    )

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
    test_game = BattleKnights(
        size=Point(2, 2),
        knights=[Knight('R', 'red', KnightState(Point(0, 0))),
                 Knight('B', 'blue', KnightState(Point(1, 1)))],
        items=[]
    )
    status = test_game.game_step('R', 'N')
    assert status['red'].status == 'DROWNED'

    status = test_game.game_step('R', 'S')
    assert status['red'].status == 'DROWNED'
