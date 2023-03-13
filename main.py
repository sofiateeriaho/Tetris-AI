""" Main script to either train deep q-learning agent or test deep q-learning agent

Train agent using random exploration
    - train.train_agent('tetris_random.h5')
Train agent using helper function
    - train.train_agent('tetris_helper.h5')

* note : the training process starts with exploration

Test agent using random exploration
    - test.test_agent('tetris_random.h5')
Test agent using helper function
    - test.test_agent('tetris_helper.h5')
"""

import train
import test

if __name__ == '__main__':

    train.train_agent('tetris_helper.h5')


