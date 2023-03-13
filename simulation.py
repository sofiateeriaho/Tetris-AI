'''Function to simulate the placement of pieces to extract resulting board features'''

import copy
import numpy as np

'''Check for intersection in test environment'''
def test_intersects(piece, field, y, x):

    intersection = False

    if len(piece) + y >= len(field) or len(piece[0]) + x >= len(field[0]) + 1 or x < 0 or y < 0:
        intersection = True

    for i in range(len(piece)):
        for j in range(len(piece[0])):
            if piece[i][j] > 0:
                if field[i + y][j + x] > 0:
                    y -= 1
                    intersection = True

    return intersection, y


def test_update_board(y, x, field, piece):

    f = copy.deepcopy(field)

    for i in range(len(piece)):
        for j in range(len(piece[0])):
            if piece[i][j] > 0:
                f[i + y][j + x] = piece[i][j]

    return f

'''Get all possible next states'''
def get_next_states(piece, field):

    # initialize dictionary
    states = {}

    if any(7 in row for row in piece):
        rotations = [0]
    elif any(6 in row for row in piece):
        rotations = [0, 1]
    else:
        rotations = [0, 1, 2, 3]

    piece = np.rot90(piece, 1)

    # for all rotations
    for rotation in rotations:
        piece = np.rot90(piece, 3)

        for x in range(len(field[0]) - len(piece[0]) + 1):

            m = count_max_height(field)

            # set limit so pieces do not get stuck in top left, top right positions
            if len(piece) + m < len(field):
                if x >= 2 or x <= 17:

                    for y in range(len(field) - len(piece) + 1):
                        intersects, y2 = test_intersects(piece, field, y, x)
                        if intersects:
                            if y2 != y:
                                updated_board = test_update_board(y2, x, field, piece)
                                states[(x, rotation)] = get_board_props(updated_board, y2)
                            else:
                                updated_board = test_update_board(y, x, field, piece)
                                states[(x, rotation)] = get_board_props(updated_board, y)
                            # to visualise state use np.array
                            # states[(x, rotation)] = np.array(updated_board)
                            break
    return states

def count_max_height(board):

    board_height = len(board)

    for i, row in enumerate(board):
        if any(val > 0 for val in row):
            return board_height - i
    return 0

'''Get all board features'''
def get_board_props(board, y):

    landing_height = len(board) - y
    cells_cleared = count_cells_cleared(board)
    row_t, col_t = row_col_transitions(board)
    holes = count_holes(board)
    wells = count_wells(board)

    return [landing_height, cells_cleared, row_t, col_t, holes, wells]

'''Count no. of empty cells covered by a full cell'''
def count_holes(board):

    holes = 0
    board_height = len(board)

    for col in zip(*board):
        i = 0
        while i < board_height and col[i] == 0:
            i += 1
        holes += len([x for x in col[i+1:] if x == 0])

    return holes

'''Count no. of columns with at least one cell such that its left and right cells are both full.'''
def count_wells(board):

    rows = len(board)
    cols = len(board[0])
    wells = 0

    for j in range(cols):
        for i in range(rows):
            if board[i][j] > 0:
                break
            if board[i][j] == 0:
                # check first column
                if j == 0 and board[i][j+1] > 0:
                    wells += 1
                    break
                # check last column
                if j == cols-1 and board[i][j-1] > 0:
                    wells += 1
                    break
                if (j > 0 and board[i][j-1] > 0) and (j < cols-1 and board[i][j+1] > 0):
                    wells += 1
                    break
    return wells

'''Count no. rows with no empty cells'''
def count_cells_cleared(board):

    return sum([all(val > 0 for val in row) for row in board]) * len(board[0])

'''Y-coordinate of the placed piece'''
def landing_height(y):

    return y

'''Count no. of empty cells horizontally/vertically adjacent to filled cells or vice versa'''
def row_col_transitions(board):

    rows = len(board)
    cols = len(board[0])

    row_transitions = 0
    col_transitions = 0

    for i in range(rows):
        for j in range(cols):
            if j > 0:
                if board[i][j] == 0 and board[i][j-1] > 0:
                    row_transitions += 1
                if board[i][j] > 0 and board[i][j - 1] == 0:
                    row_transitions += 1
            if i > 0:
                if board[i][j] == 0 and board[i-1][j] > 0:
                    col_transitions += 1
                if board[i][j] > 0 and board[i-1][j] == 0:
                    col_transitions += 1

    return row_transitions, col_transitions



