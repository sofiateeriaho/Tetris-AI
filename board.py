'''Function to define board and control gameplay'''

from tetromino import Tetromino
import copy
import simulation
import random

class Board():

    def __init__(self):
        self.width = 10
        self.height = 20
        self.reset()

    '''Resets game, board is cleared'''
    def reset(self):

        self.score = 0
        self.total_lines_cleared = 0
        self.tetrises = 0
        self.game_over = False
        self.state = []

        # create empty board
        for i in range(self.height):
            new_line = []
            for j in range(self.width):
                new_line.append(0)
            self.state.append(new_line)

        self.bag = []
        self.new_round()

        return simulation.get_board_props(self.state, 20)

    # Choose random tetromino from list of tetrominoes
    def choose_random(self):
        return random.randint(0, 7)

    # No tetromino is repeatedly drawn until all tetrominoes have been used
    def choose_random_bag(self):
        if len(self.bag) <= 0:
            self.bag = list(range(7))

        self.bag = random.shuffle(self.bag)
        r = self.bag.pop()
        return r

    '''Create copy of game state'''
    def deep_copy(self):
        return copy.deepcopy(self)

    '''Generate new random piece'''
    def new_piece(self):

        self.bag = list(range(7))
        random.shuffle(self.bag)

        self.current_piece = Tetromino(4, 0, self.bag.pop())

    '''Checks if piece intersects with board or other pieces'''
    def intersects(self):

        intersection = False

        # intersects with board
        if self.current_piece.height() + self.current_piece.y >= self.height or self.current_piece.width() + self.current_piece.x >= self.width + 1 or self.current_piece.x < 0 or self.current_piece.y < 0:
            intersection = True

        # intersects with another tetromino
        for i in reversed(range(self.current_piece.height())):
            for j in range(self.current_piece.width()):
                if self.current_piece.get_state()[i][j] > 0:
                    if self.state[i + self.current_piece.y][j + self.current_piece.x] > 0:
                        self.current_piece.y -= 1
                        intersection = True

        return intersection

    '''Controls descent of piece'''
    def go_down(self):

        self.current_piece.y += 1

        if self.intersects():
            self.place_piece()

    '''Places piece on board'''
    def place_piece(self):

        self.update_board()
        lines = self.clear_lines()
        self.update_score(lines)
        self.round_done = True

    '''Starts new round'''
    def new_round(self):
        self.round_done = False
        self.new_piece()

        # if the piece intersects the game is over
        if self.intersects():
            self.game_over = True

    '''When row is full (all cells filled), eliminates row and moves top pieces down by one coordinate'''
    def clear_lines(self):

        lines = 0

        for i in range(1, self.height):
            zeros = 0
            for j in range(self.width):
                if self.state[i][j] == 0:
                    zeros += 1
            if zeros == 0:
                lines += 1
                for i1 in range(i, 1, -1):
                    for j in range(self.width):
                        self.state[i1][j] = self.state[i1 - 1][j]

        self.total_lines_cleared += lines

        if lines == 4:
            self.tetrises += 1

        return lines

    '''Updates score based on values'''
    def update_score(self, lines):
        points = [0, 40, 100, 300, 1200]
        self.score += points[lines]

    '''Updates board once piece is placed'''
    def update_board(self):
        for i in range(self.current_piece.height()):
            for j in range(self.current_piece.width()):
                if self.current_piece.get_state()[i][j] > 0:
                    self.state[i + self.current_piece.y][j + self.current_piece.x] = self.current_piece.get_state()[i][j]

    '''Moves piece left or right'''
    def move(self, direction):

        # 1 is right, -1 is left
        self.current_piece.x += direction

    '''Rotates piece'''
    def rotate(self):

        self.current_piece.rotate()

