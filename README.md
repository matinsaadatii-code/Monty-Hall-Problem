# Monty Hall Problem

**Programmer:** Matin Saadatii

- **LinkedIn:** [Matin Saadatii](https://www.linkedin.com/in/matin-saadatii/)
- **Website:** [matechs.ir](https://matechs.ir)
- **Telegram:** [@sMATINss](https://t.me/sMATINss)

---

An interactive Python project that demonstrates the famous **Monty Hall problem**. It includes a command-line game, a Monte Carlo simulation, and a Streamlit dashboard where you can play the game yourself and watch the simulation converge live.

## The Problem

You are on a game show with three doors. Behind one is a car, behind the other two are goats.

1. You pick a door.
2. The host (Monty), who knows what is behind every door, opens one of the other doors and reveals a goat.
3. You are offered the chance to **switch** to the remaining closed door or **stay** with your original pick.

Should you switch?

**Yes.** Your first pick is right only 1/3 of the time, and Monty's reveal does not change that. So the remaining door holds the car with probability 2/3.

| Strategy          | Theoretical win probability |
| ----------------- | --------------------------- |
| Stay (no switch)  | 1/3 ≈ 33.3%                 |
| Switch            | 2/3 ≈ 66.7%                 |

## Features

- **Monte Carlo simulation** of both strategies (staying vs. switching)
- **Interactive command-line game** with input validation
- **Streamlit dashboard** with two tabs:
  - **Game**: play step by step with buttons and a running score
  - **Simulation**: choose the number of games and watch the win rates of both strategies converge on one chart
- Game logic is separated from input/output, so the same functions are reused by the CLI and the GUI

## Project Structure

```
.
├── main.py      # MontyHallGame class (logic, simulation, CLI game)
├── app.py       # Streamlit dashboard
└── README.md
```

## Requirements

- Python **3.12+** (the CLI code uses nested quotes inside f-strings)
- [Streamlit](https://streamlit.io/)

## Installation

```bash
git clone <your-repository-url>
cd <your-repository-folder>

python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate

pip install streamlit
```

## Usage

### Command line

```bash
python main.py
```

You will be asked for the number of games to simulate. The program prints the winning percentage with and without switching, then starts one interactive game in the terminal.

### Streamlit dashboard

```bash
streamlit run app.py
```

Then open the local URL shown in the terminal (usually http://localhost:8501).

- **Game tab**: choose a door, see which door Monty opens, then decide to switch or stay. Your score is tracked across rounds.
- **Simulation tab**: set the number of simulations (1 to 10,000) and watch both win rates converge toward 1/3 and 2/3.

## How It Works

### `MontyHallGame` (in `main.py`)

| Method                  | Description                                                                 |
| ----------------------- | --------------------------------------------------------------------------- |
| `monty_hall_simulation` | Simulates one game with a given strategy (`switch_doors=True/False`)        |
| `simulate_games`        | Runs many games for both strategies and returns the number of wins of each  |
| `cmd_monty_hall_game`   | Plays one interactive game in the terminal                                  |
| `gui_new_game`          | Returns a freshly shuffled set of doors                                     |
| `gui_reveal_goat`       | Picks a goat door for Monty to open (never the player's door)               |
| `gui_final_choice`      | Returns the final door depending on whether the player switches             |

### Why the GUI functions are separate

Streamlit re-runs the whole script on every interaction, so a function that blocks on `input()` cannot work in a web UI. The GUI game is split into small steps (`choose` → `switch` → `result`), and the current state is stored in `st.session_state`.

## Example Results

With enough simulations the results approach the theoretical values:

```
Winning percentage without switching doors: 33.41%
Winning percentage with    switching doors: 66.87%
```

Small games fluctuate a lot at the beginning (the law of large numbers), then stabilize as the number of games grows.

## Contact

If you have questions or suggestions, reach out via any of the links at the top of this file.