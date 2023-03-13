'''Function to define tetrominoes'''

import numpy as np

class Tetromino():

    colors = [
        # purple
        (138, 43, 226),
        # green
        (118, 238, 0),
        # red
        (238, 44, 44),
        # blue
        (0,0,255),
        # orange
        (255,153,18),
        # light blue
        (142,229,238),
        # yellow
        (238,201,0),
    ]

    tetrominoes = [
        # T
        [[0, 1, 0],
         [1, 1, 1]],
        # S
        [[0, 2, 2],
         [2, 2, 0]],
        # Z
        [[3, 3, 0],
         [0, 3, 3]],
        # J
        [[4, 0, 0],
         [4, 4, 4]],
        # L
        [[0, 0, 5],
         [5, 5, 5]],
        # I
        [[6, 6, 6, 6]],
        # O
        [[7, 7],
         [7, 7]]
    ]

    def __init__(self, x, y, rand_piece):
        # left most row coordinate
        self.x = x
        # left most col coordinate
        self.y = y

        self.rotation = 0

        self.color = self.colors[rand_piece]
        self.state = self.tetrominoes[rand_piece]

    def get_state(self):
        return self.state

    '''Returns width of tetromino'''
    def width(self):
        s = np.array(self.state)
        return s.shape[1]

    '''Returns height of tetromino'''
    def height(self):
        s = np.array(self.state)
        return s.shape[0]

    '''Rotates piece by 90 degree increments'''
    def rotate(self):
        self.rotate_right()
        self.rotation = (self.rotation + 1) % 4

    def rotate_right(self):
        self.state = np.rot90(self.state, 3)
        return self

