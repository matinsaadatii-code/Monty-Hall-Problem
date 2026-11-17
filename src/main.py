import random


class MontyHallGame():
    def __init__(self):
        self.doors = ['car'] + ['goat'] * 2


    def monty_hall_simulation(self, switch_doors: bool) -> bool:
        """
        Simulate a single Monty Hall game.

        :param bool switch_doors: If True, the contestant will switch their choice after a goat door is revealed.
        :return: True if the contestant won the car, False otherwise.
        :rtype: bool
        """

        # Initialize doors with one having a car and the rest goats
        random.shuffle(self.doors)

        # Contestant selects a door initially
        initial_choice = random.choice(range(len(self.doors)))

        # Monty reveals a door with a goat
        doors_revealed = [i for i in range(len(self.doors)) if (i != initial_choice) and (self.doors[i] == 'goat')]
        door_revealed = random.choice(doors_revealed)

        # If contestant decides to switch, their final choice is the remaining door
        if switch_doors:
            final_choice = [i for i in range(len(self.doors)) if (i != initial_choice) and (i != door_revealed)][0]
        else:
            # Keep the initial choice
            final_choice = initial_choice

        # Return if contestant won the car
        return self.doors[final_choice] == 'car'

    def cmd_monty_hall_game(self) -> bool:
        """
        Play one interactive Monty Hall game.

        :return: True if the player won the car, False otherwise.
        :rtype: bool
        """

        random.shuffle(self.doors)

        while True:
            try:
                initial_choice: int = int(input(f'Choose a Door ({', '.join(str(i + 1) for i, _ in enumerate(self.doors))}): ')) - 1
            except ValueError:
                print('Enter a number.')
                continue

            if not 0 <= initial_choice < len(self.doors):
                print(f'Door must be between 1 and {len(self.doors)}.')
                continue

            break

        doors_revealed = [
            i for i in range(len(self.doors)) 
            if (i != initial_choice) and (self.doors[i] == 'goat')
        ]
        door_revealed = random.choice(doors_revealed)

        print(f'Monty opened the Door {door_revealed + 1} and there was a {self.doors[door_revealed]} behind it.')


        while True:
            switch_doors_choice: str = input('You want to change door (yes/no): ').strip().lower()

            if switch_doors_choice == 'yes':
                final_choice = [i for i in range(len(self.doors)) if (i != initial_choice) and (i != door_revealed)][0]
                break
            elif switch_doors_choice == 'no':
                final_choice = initial_choice
                break
                
            print('Enter yes or no.')                    

        won = self.doors[final_choice] == 'car'

        print('You won the car!' if won else 'You got the Goat!')
        return won

    def gui_new_game(self) -> list[str]:
        doors = self.doors.copy()
        random.shuffle(doors)
        return doors

    def gui_reveal_goat(self, doors: list[str], initial_choice: int) -> int:
        options = [
            i for i in range(len(doors))
            if i != initial_choice and doors[i] == 'goat'
        ]
        return random.choice(options)

    def gui_final_choice(self, doors, initial_choice, door_revealed, switch: bool) -> int:
        if not switch:
            return initial_choice
        return next(
            i for i in range(len(doors))
            if i != initial_choice and i != door_revealed
        )


    def simulate_games(self, num_games: int = 1000) -> None:
        """
        Simulate a number of Monty Hall games and print the statistics.

        :param int num_games: The number of games to simulate. Defaults to 1000.
        :return: None
        """

        # Simulate games where contestant keeps and switches doors
        num_wins_without_switching = sum(self.monty_hall_simulation(switch_doors=False) for _ in range(num_games))
        num_wins_with_switching = sum(self.monty_hall_simulation(switch_doors=True) for _ in range(num_games))

        return num_wins_without_switching, num_wins_with_switching


if __name__ == "__main__":
    mhg = MontyHallGame()
    num_games = int(input('Enter number of games: '))
    num_wins_without_switching, num_wins_with_switching = mhg.simulate_games(num_games)

    print(f"Winning percentage without switching doors: {(num_wins_without_switching/num_games):.2%}")
    print(f"Winning percentage with    switching doors: {(num_wins_with_switching/num_games):.2%}")

    mhg.cmd_monty_hall_game()
