from server.character import Character


def test_character() -> None:
    my_char = Character(name='Harry Potter', health=90, magic_rate=14, strike_rate=10,
                        defence_rate=20, magic_reset_rate=12, power=50)
    assert my_char.name == 'Harry Potter'
    assert my_char.magic_rate == 14
    assert my_char.strike_rate == 10
    assert my_char.defence_rate == 20
    assert my_char.magic_reset_rate == 12
    assert my_char.power == 50


def test_character_reduce_health() -> None:
    my_char = Character(name='Harry Potter', health=90, magic_rate=14, strike_rate=10,
                        defence_rate=20, magic_reset_rate=12, power=50)
    my_char.reduce_health(100)
    assert my_char.health == 0


def test_character_increase_magic() -> None:
    my_char = Character(name='Harry Potter', health=90, magic_rate=14, strike_rate=10,
                        defence_rate=20, magic_reset_rate=12, power=50)
    before_magic = my_char.magic
    my_char.increase_magic()
    assert before_magic == my_char.magic - my_char.magic_reset_rate
