'''Function to visualise gameplay using pygame library'''

import pygame
import sys
import plotly.graph_objects as go

top_left_x = 53
top_left_y = 50
block_size = 20

screen_width = 400
screen_height = 500

# initialize the game engine
pygame.init()

# define some colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GRAY = (193, 205, 205)

# create window screen
screen = pygame.display.set_mode((screen_width, screen_height))

# create window name
pygame.display.set_caption("My Bachelor Project: Tetris")

def visualise_pygame(game, episode, best_action):

    # control framerate
    clock = pygame.time.Clock()
    paused = False
    speed = 300

    # create the game loop
    while not game.round_done:

        for event in list(pygame.event.get()):
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and paused:
                    paused = False
                elif event.key == pygame.K_SPACE or game.tetrises == 1:
                    paused = True

        if not paused:

            if game.current_piece.x != best_action[0] or game.current_piece.rotation != best_action[1]:

                if game.current_piece.rotation != best_action[1]:
                    game.rotate()
                if game.current_piece.x < best_action[0]:
                    game.move(1)
                if game.current_piece.x > best_action[0]:
                    game.move(-1)

            else:
                game.go_down()

            font2 = pygame.font.SysFont('Calibri', 14, True, False)
            text3 = font2.render("Press SPACE to pause", True, GRAY)
        else:
            font2 = pygame.font.SysFont('Calibri', 14, True, False)
            text3 = font2.render("Game Paused, press SPACE to continue", True, GRAY)

        screen.fill(WHITE)

        # draw board
        for i in range(game.height):
            for j in range(game.width):
                pygame.draw.rect(screen, GRAY, [top_left_x + block_size * j, top_left_y + block_size * i, block_size, block_size], 1)
                if game.state[i][j] > 0:
                    color_index = game.state[i][j]
                    pygame.draw.rect(screen, game.current_piece.colors[color_index-1], (to_screen_size_x(j), to_screen_size_y(i), block_size, block_size), 0)

        if not game.game_over:
            piece_shape = game.current_piece.get_state()
            # draw shape on board
            for y in range(len(piece_shape)):
                for x in range(len(piece_shape[y])):
                    if piece_shape[y][x] > 0:
                        pygame.draw.rect(screen, game.current_piece.color, (to_screen_size_x(game.current_piece.x + x), to_screen_size_y(game.current_piece.y + y), block_size, block_size), 0)

        font = pygame.font.SysFont('Calibri', 18, True, False)

        text = font.render("Score: " + str(game.score), True, BLACK)
        text1 = font.render("Lines: " + str(game.total_lines_cleared), True, BLACK)
        text2 = font.render("Episode: " + str(episode), True, BLACK)

        screen.blit(text, [270, 100])
        screen.blit(text1, [270, 130])
        screen.blit(text2, [270, 200])
        screen.blit(text3, [60, 465])

        pygame.display.flip()
        clock.tick(speed)


'''Calculates the pixel coordinates for pygame:
given the x and y coordinate of piece x : 0 - 10 and y : 0 - 20'''
def to_screen_size_x(x):
    return (block_size * x) + top_left_x

def to_screen_size_y(y):
    return (block_size * y) + top_left_y

'''Displays average, minimum, maximum scores from batch of scores'''
def display_train(episodes_count, min_scores, max_scores, avg_scores):
    fig = go.Figure()

    fig.update_layout(
        title="Training Progress",
        xaxis_title="Episodes Count",
        yaxis_title="Scores"
    )

    fig.add_trace(go.Scatter(
        x=episodes_count,
        y=min_scores,
        mode="lines+markers",
        name="Minimum score",
    ))

    fig.add_trace(go.Scatter(
        x=episodes_count,
        y=max_scores,
        mode="lines+markers",
        name="Maximum score",
    ))

    fig.add_trace(go.Scatter(
        x=episodes_count,
        y=avg_scores,
        mode="lines+markers",
        name="Average score",
    ))

    fig.show()

'''Displays scores'''
def display_test(episodes_count, scores):
    fig = go.Figure()

    fig.update_layout(
        title="Testing Progress",
        xaxis_title="Episodes Count",
        yaxis_title="Scores"
    )

    fig.add_trace(go.Scatter(
        x=episodes_count,
        y=scores,
        mode="lines+markers",
        name="Score",
    ))

    fig.show()

