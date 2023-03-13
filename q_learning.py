'''Function for Deep Q Learning Agent

References:
    Nguyen, V (2020) [PYTORCH] Deep Q-learning for playing Tetris. https://github.com/uvipen/Tetris-deep-Q-learning-pytorch '''


import numpy as np
import random
from collections import deque

from tensorflow.keras.models import Sequential, save_model, load_model
from tensorflow.keras.layers import Dense
from tensorflow.keras.optimizers import Adam

class DQNAgent:
    '''Deep Q Learning Agent
    Args:
        state_size (int): Size of the input domain
        mem_size (int): Size of the replay buffer
        discount (float): How important is the future rewards compared to the immediate ones [0,1]
        epsilon (float): Exploration (probability of random values given) value at the start
        epsilon_min (float): At what epsilon value the agent stops decrementing it
        epsilon_stop_episode (int): At what episode the agent stops decreasing the exploration variable
        n_neurons (list(int)): List with the number of neurons in each inner layer
        activations (list): List with the activations used in each inner layer, as well as the output
        loss (obj): Loss function
        optimizer (obj): Optimizer used
        replay_start_size: Minimum size needed to train
    '''

    def __init__(self, state_size=6, mem_size=1000000, discount=0.8,
                 epsilon=1, epsilon_min=0, epsilon_stop_episode=500,
                 n_neurons=[64, 64], activations=['relu', 'relu', 'linear'],
                 loss='mse', optimizer=Adam(lr=0.001)):

        assert len(activations) == len(n_neurons) + 1

        self.state_size = state_size
        self.memory = deque(maxlen=mem_size)
        self.discount = discount
        self.epsilon = epsilon
        self.epsilon_min = epsilon_min
        self.epsilon_decay = self.epsilon / epsilon_stop_episode
        self.n_neurons = n_neurons
        self.activations = activations
        self.loss = loss
        self.optimizer = optimizer
        self.model = self.build_model()

    '''Builds a Keras deep neural network model'''
    def build_model(self):

        model = Sequential()
        model.add(Dense(self.n_neurons[0], input_dim=self.state_size, activation=self.activations[0]))

        for i in range(1, len(self.n_neurons)):
            model.add(Dense(self.n_neurons[i], activation=self.activations[i]))

        model.add(Dense(1, activation=self.activations[-1]))

        model.compile(loss=self.loss, optimizer=self.optimizer)
        print(model.summary())

        return model

    '''Adds a play to the replay memory buffer'''
    def add_to_memory(self, current_state, next_state, reward, done):

        self.memory.append((current_state, next_state, reward, done))

    '''Predicts the score for a certain state'''
    def predict_value(self, state):

        return self.model.predict(state)[0]

    '''Choses random state or predicts the best state for a given collection of states'''
    def best_state_explore(self, states):

        max_value = None
        best_state = None

        if random.random() <= self.epsilon:
            return random.choice(list(states))

        else:
            for state in states:
                value = self.predict_value(np.reshape(state, [1, self.state_size]))
                if not max_value or value > max_value:
                    max_value = value
                    best_state = state

        return best_state

    '''Predicts the best state for a given collection of states'''
    def best_state_test(self, states):

        max_value = None
        best_state = None

        for state in states:
            value = self.predict_value(np.reshape(state, [1, self.state_size]))
            if not max_value or value > max_value:
                max_value = value
                best_state = state

        return best_state

    '''Predicts a 'good' state by assigning weights to features'''
    def best_state_helper(self, states):

        max_value = 0

        for state in states:

            total_value = 0
            for feature in range(len(state)):
                if feature == 1:
                    total_value += 10 * state[feature]
                elif feature == 2 or feature == 3:
                    total_value += 100 - state[feature]
                elif feature == 4:
                    total_value += 50 - state[feature]
                elif feature == 5:
                    total_value += state[feature]

            if total_value > max_value:
                max_value = total_value
                best_state = state

        return best_state

    '''Trains by batches'''
    def train(self, batch_size=32, epochs=3):

        n = len(self.memory)

        if n >= batch_size:

            batch = random.sample(self.memory, batch_size)

            # get the expected score for the next states, in batch (better performance)
            next_states = np.array([x[1] for x in batch])
            next_qs = [x[0] for x in self.model.predict(next_states)]

            x = []
            y = []

            # build xy structure to fit the model in batch (better performance)
            for i, (state, _, reward, done) in enumerate(batch):
                if not done:
                    # Partial Q formula
                    new_q = reward + self.discount * next_qs[i]
                else:
                    new_q = reward

                x.append(state)
                y.append(new_q)

            # fit the model to the given values
            self.model.fit(np.array(x), np.array(y), batch_size=batch_size, epochs=epochs, verbose=0)

            # update the exploration variable
            if self.epsilon > self.epsilon_min:
                self.epsilon -= self.epsilon_decay

    '''Loads weights from file'''
    def load(self, name):
        self.model.load_weights(name)
        print(self.epsilon_decay)

    '''Saves weights to file'''
    def save(self, name):
        self.model.save_weights(name)