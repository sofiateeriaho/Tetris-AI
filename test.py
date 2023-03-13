'''Function to test agent's performance

- loads weights from existing file
- cannot test if no file to load weights from'''

import visualise
import board
import q_learning
import simulation
import os.path
from os import path

def test_agent(file):

    # Check for previous models
    output_dir = "model_output/"
    if not os.path.exists(output_dir):
        print("No previous model to test. \n Train model first.")

    file_dir = output_dir + file

    if path.exists(file_dir):

        # initialize board and agent
        game = board.Board()
        agent = q_learning.DQNAgent()

        agent.load(file_dir)
        print("Model loaded")

        scores = []
        episodes_plot = []

        for i in range(1, 10):

            game.reset()
            steps = 0

            while not game.game_over or steps < 507:
                steps += 1

                game_copy = game.deep_copy()

                p = game_copy.current_piece.get_state()
                f = game_copy.state

                next_states = simulation.get_next_states(p, f)

                if len(next_states) > 0:

                    best_state = agent.best_state_test(next_states.values())

                    best_action = None
                    for action, state in next_states.items():
                        if state == best_state:
                            best_action = action
                            break

                    visualise.visualise_pygame(game, i, best_action)

                    game.new_round()
                else:
                    game.game_over = True

            scores.append(game.score)
            episodes_plot.append(i)

    else:
        print("No previous model to test. \n Train model first.")

    visualise.display_test(episodes_plot, scores)