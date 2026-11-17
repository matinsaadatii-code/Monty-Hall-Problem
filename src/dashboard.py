import streamlit as st
import time

from main import MontyHallGame

mhg = MontyHallGame()

st.title('Monty Hall Problem')

tab_game, tab_sim = st.tabs(['Game', 'Simulation'])

with tab_game:
    st.header('Game')

    if 'game' not in st.session_state:
        st.session_state.game = {
            'stage': 'choose',
            'doors': mhg.gui_new_game(),
            'initial': None,
            'revealed': None,
            'final': None,
        }
        st.session_state.wins = 0
        st.session_state.played = 0

    g = st.session_state.game
    n = len(g['doors'])

    if g['stage'] == 'choose':
        st.write('Choose a door:')
        cols = st.columns(n)
        for i, col in enumerate(cols):
            if col.button(f'🚪 Door {i + 1}', key=f'door_{i}', use_container_width=True):
                g['initial'] = i
                g['revealed'] = mhg.gui_reveal_goat(g['doors'], i)
                g['stage'] = 'switch'
                st.rerun()

    elif g['stage'] == 'switch':
        st.write(f"You chose Door {g['initial'] + 1}.")
        st.write(
            f"Monty opened Door {g['revealed'] + 1} "
            f"and there was a {g['doors'][g['revealed']]} behind it."
        )
        c1, c2 = st.columns(2)
        if c1.button('Switch', use_container_width=True):
            g['final'] = mhg.gui_final_choice(g['doors'], g['initial'], g['revealed'], True)
            g['stage'] = 'result'
            st.rerun()
        if c2.button('Stay', use_container_width=True):
            g['final'] = mhg.gui_final_choice(g['doors'], g['initial'], g['revealed'], False)
            g['stage'] = 'result'
            st.rerun()

    elif g['stage'] == 'result':
        won = g['doors'][g['final']] == 'car'
        st.session_state.played += 1
        st.session_state.wins += won

        if won:
            st.success('You won the car! 🚗')
        else:
            st.error('You got the goat! 🐐')

        st.write('Doors: ' + ' | '.join(
            f'{i + 1}: {d}' for i, d in enumerate(g['doors'])
        ))

        if st.button('Play again'):
            st.session_state.game = {
                'stage': 'choose',
                'doors': mhg.gui_new_game(),
                'initial': None, 'revealed': None, 'final': None,
            }
            st.rerun()

    st.metric(
        'Score',
        f"{st.session_state.wins} / {st.session_state.played}",
    )

with tab_sim:
    st.header('Simulation')

    number_games: int = st.number_input('Number of Simulations', 
    min_value=1, max_value=10000, value=100, step=1, key='num_simulations')

    wins_with_switching = 0
    wins_without_switching = 0

    chart = st.empty()

    rates_with_switching = []
    rates_without_switching = []

    for i in range(number_games):
        simulations_without_switching, simulations_with_switching = (
            mhg.simulate_games(num_games=1)
        )

        wins_with_switching += simulations_with_switching
        wins_without_switching += simulations_without_switching

        rates_without_switching.append(
            wins_without_switching / (i + 1)
        )

        rates_with_switching.append(
            wins_with_switching / (i + 1)
        )

        chart.line_chart({
        'Without Switching': rates_without_switching,
        'With Switching': rates_with_switching,
        })

        time.sleep(0.1)
