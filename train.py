'''Function to train deep q-learning agent

- if file exists, continues adjusting already learned weights
- if file does not exist, creates a new file'''

import visualise
import board
import q_learning
import simulation
from statistics import mean
import os.path
from os import path

def train_agent(file):

    scores_every = 10
    save_every = 20
    display_every = 300

    # Create model
    output_dir = "model_output/"
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    file_dir = output_dir + file

    # Define batch size and epochs for training
    batch_size = 100
    epochs = 5

    # Load agent and board
    game = board.Board()
    agent = q_learning.DQNAgent()

    # If model already exists, load existing model
    if path.exists(file_dir):
        print("Previous model loaded")
        agent.load(file_dir)

    # Create empty lists for storing scores
    scores = []
    episodes_plot = []
    min_scores = []
    max_scores = []
    avg_scores = []

    # Train for 1k episodes, agents plays 1k games
    for i in range(1, 1001):

        # Start new game
        current_state = game.reset()

        steps = 0

        # game ends when pieces reach the top of board or steps reach limit
        while not game.game_over and steps < 507:
            steps += 1

            game_copy = game.deep_copy()

            p = game_copy.current_piece.get_state()
            f = game_copy.state

            next_states = simulation.get_next_states(p, f)

            if len(next_states) > 0:

                if file == 'tetris_random.h5':
                    best_state = agent.best_state_explore(next_states.values())
                else:
                    best_state = agent.best_state_helper(next_states.values())

                best_action = None
                for action, state in next_states.items():
                    if state == best_state:
                        best_action = action
                        break

                # visualise game board with chosen action in pygame
                visualise.visualise_pygame(game, i, best_action)

                agent.add_to_memory(current_state, next_states[best_action], game.score, game.game_over)
                current_state = next_states[best_action]

                game.new_round()
            else:
                game.game_over = True
                agent.add_to_memory(current_state, current_state, -2, game.game_over)

        agent.train(batch_size=batch_size, epochs=epochs)

        scores.append(game.score)


        if i % scores_every == 0:
            episodes_plot.append(i)
            min_scores.append(min(scores))
            max_scores.append(max(scores))
            avg_scores.append(mean(scores))
            scores = []

        if i % save_every == 0:
            agent.save(file_dir)

        if i % display_every == 0:
            visualise.display_train(episodes_plot, min_scores, max_scores, avg_scores)

    visualise.display_train(episodes_plot, min_scores, max_scores, avg_scores)





