from app.main import BattleKnights, Knight, KnightState, Point


def test_movement():
    test_game = BattleKnights(
        (2, 2),
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

