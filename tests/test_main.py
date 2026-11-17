import pytest
from unittest.mock import patch
from io import StringIO

from src import main


DOORS = ['goat', 'car', 'goat']


def run(game, inputs):
    with patch('builtins.input', side_effect=inputs), \
         patch('random.shuffle'), \
         patch('sys.stdout', new_callable=StringIO) as out:
        result = game.cmd_monty_hall_game()
    return result, out.getvalue()


def test_simulate_games(game):
    number_of_games = 1000
    wins_without_switching, wins_with_switching = game.simulate_games(num_games=number_of_games)

    assert isinstance(wins_without_switching, int)
    assert isinstance(wins_with_switching, int)
    assert 0 <= wins_without_switching <= number_of_games
    assert 0 <= wins_with_switching <= number_of_games


def test_simulate_games_one(game):
    wins_without_switching, wins_with_switching = game.simulate_games(num_games=1)

    assert isinstance(wins_without_switching, int)
    assert isinstance(wins_with_switching, int)
    assert 0 <= wins_without_switching <= 1
    assert 0 <= wins_with_switching <= 1


def test_fails_simulate_game_invalid_values(game):
    with pytest.raises(ValueError, match='Invalid number'):
        game.simulate_games(num_games='bad')
    

def test_monty_hall_simulation(game):
    result_with_switching = game.monty_hall_simulation(switch_doors=True)
    result_without_switching = game.monty_hall_simulation(switch_doors=False)

    assert isinstance(result_with_switching, bool)
    assert isinstance(result_without_switching, bool)


def test_fails_monty_hall_simulation(game):
    with pytest.raises(ValueError, match='Invalid arg. Please Enter between True or False'):
        game.monty_hall_simulation(switch_doors='abc')


def test_switch_from_goat_wins(game):
    result, _ = run(game, ['1', 'yes'])

    assert result is True


def test_switch_from_car_loses(game):
    result, out = run(game, ['2', 'yes'])

    assert result is False
    assert 'You got the Goat!' in out


def test_stay_with_car_wins(game):
    result, out = run(game, ['2', 'no'])

    assert result is True
    assert 'You won the car!' in out


def test_stay_with_goat_loses(game):
    result, _ = run(game, ['1', 'no'])

    assert result is False


def test_non_numeric_door_reprompts(game):
    result, out = run(game, ['abc', '2', 'no'])

    assert 'Enter a number.' in out
    assert result is True


@pytest.mark.parametrize('bad', ['0', '4', '-1'])
def test_out_of_range_door_reprompts(game, bad):
    result, out = run(game, [bad, '2', 'no'])

    assert 'Door must be between 1 and 3.' in out
    assert result is True


def test_invalid_yes_no_reprompts(game):
    result, out = run(game, ['1', 'maybe', 'yes'])

    assert 'Enter yes or no.' in out
    assert result is True


def test_yes_no_is_case_and_space_insensitive(game):
    result, _ = run(game, ['1', '  YES  '])

    assert result is True

def test_revealed_door_is_goat_and_not_player_choice(game):
    with patch('builtins.input', side_effect=['1', 'no']), \
         patch('random.shuffle'), \
         patch('sys.stdout', new_callable=StringIO) as out:
        game.cmd_monty_hall_game()

    assert 'Monty opened the Door 3 and there was a goat behind it.' in out.getvalue()


def test_doors_are_shuffled(game):
    with patch('builtins.input', side_effect=['1', 'no']), \
         patch('random.shuffle') as shuffle:
        game.cmd_monty_hall_game()

    shuffle.assert_called_once_with(game.doors)


def test_switching_win_rate_is_about_two_thirds():
    import random

    random.seed(42)

    g = main.MontyHallGame()
    wins = 0
    n = 5000

    for _ in range(n):
        g.doors = ['goat', 'goat', 'car']

        with patch('builtins.input', side_effect=['1', 'yes']), \
             patch('sys.stdout', new_callable=StringIO):
            wins += g.cmd_monty_hall_game()

    assert 0.63 < wins / n < 0.70


def test_gui_new_game_returns_copy(game):
    game.doors = DOORS.copy()
    doors = game.gui_new_game()
    assert doors is not game.doors
    assert game.doors == DOORS          


def test_gui_new_game_keeps_same_content(game):
    game.doors = DOORS.copy()
    doors = game.gui_new_game()
    assert sorted(doors) == sorted(DOORS)


def test_gui_new_game_calls_shuffle(game):
    game.doors = DOORS.copy()
    with patch('random.shuffle') as shuffle:
        doors = game.gui_new_game()
    shuffle.assert_called_once_with(doors)


@pytest.mark.parametrize('bad', [
    [], 'abc', None,
    ['goat', 'car'],                
    ['goat', 'goat', 'goat'],      
    ['car', 'car', 'goat'],         
    ['goat', 'car', 'dog'],         
])
def test_gui_new_game_invalid_doors(game, bad):
    game.doors = bad
    with pytest.raises(ValueError):
        game.gui_new_game()


@pytest.mark.parametrize('bad', [
    [], None, ['goat', 'car'],
    ['goat', 'goat', 'goat'],
    ['car', 'car', 'goat'],
])
def test_gui_reveal_goat_invalid_doors(game, bad):
    with pytest.raises(ValueError):
        game.gui_reveal_goat(bad, 0)


@pytest.mark.parametrize('choice, expected', [
    (0, 2),    
    (2, 0),
    (1, None), 
])
def test_gui_reveal_goat_valid(game, choice, expected):
    revealed = game.gui_reveal_goat(DOORS, choice)
    assert revealed != choice
    assert DOORS[revealed] == 'goat'
    if expected is not None:
        assert revealed == expected


def test_gui_reveal_goat_random_when_car_chosen(game):
    seen = {game.gui_reveal_goat(DOORS, 1) for _ in range(100)}
    assert seen == {0, 2}


@pytest.mark.parametrize('bad', [-1, 3, 'a', None, True, 1.0])
def test_gui_reveal_goat_invalid_choice(game, bad):
    with pytest.raises(ValueError):
        game.gui_reveal_goat(DOORS, bad)


@pytest.mark.parametrize('bad', [[], None, ['goat', 'car'], ['goat', 'goat', 'goat']])
def test_gui_reveal_goat_invalid_doors(game, bad):
    with pytest.raises(ValueError):
        game.gui_reveal_goat(bad, 0)


@pytest.mark.parametrize('initial, revealed, switch, expected', [
    (0, 2, False, 0),
    (0, 2, True, 1),    
    (2, 0, False, 2),
    (2, 0, True, 1),
    (1, 0, False, 1),
    (1, 0, True, 2),   
    (1, 2, True, 0),
])
def test_gui_final_choice_valid(game, initial, revealed, switch, expected):
    assert game.gui_final_choice(DOORS, initial, revealed, switch) == expected


def test_gui_final_choice_switch_never_returns_initial_or_revealed(game):
    for initial in range(3):
        for revealed in range(3):
            if revealed == initial or DOORS[revealed] != 'goat':
                continue
            final = game.gui_final_choice(DOORS, initial, revealed, True)
            assert final not in (initial, revealed)


@pytest.mark.parametrize('bad', [-1, 3, 'a', None, True])
def test_gui_final_choice_invalid_initial(game, bad):
    with pytest.raises(ValueError):
        game.gui_final_choice(DOORS, bad, 2, True)


@pytest.mark.parametrize('bad', [-1, 3, 'a', None, True])
def test_gui_final_choice_invalid_revealed(game, bad):
    with pytest.raises(ValueError):
        game.gui_final_choice(DOORS, 0, bad, True)


def test_gui_final_choice_invalid_switch(game):
    with pytest.raises(ValueError, match='Invalid choice. '):
        game.gui_final_choice(DOORS, 0, 2, 'bad')


# def test_gui_final_choice_revealed_equals_initial(game):
#     with pytest.raises(ValueError, match='initial choice'):
#         game.gui_final_choice(DOORS, 0, 0, True)


# def test_gui_final_choice_revealed_is_car(game):
#     with pytest.raises(ValueError, match='goat'):
#         game.gui_final_choice(DOORS, 0, 1, True)


def test_gui_final_choice_invalid_doors(game):
    with pytest.raises(ValueError):
        game.gui_final_choice([], 0, 1, True)


def test_full_gui_flow_switch_wins_when_initial_is_goat(game):
    game.doors = DOORS.copy()
    doors = game.gui_new_game()
    initial = doors.index('goat')
    revealed = game.gui_reveal_goat(doors, initial)
    final = game.gui_final_choice(doors, initial, revealed, True)
    assert doors[final] == 'car'


@pytest.mark.parametrize('bad', [1, 0, None, 'yes'])
def test_gui_final_choice_invalid_switch(game, bad):
    with pytest.raises(ValueError, match='Invalid choice'):
        game.gui_final_choice(DOORS, 0, 2, bad)