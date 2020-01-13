import random
import copy
import sys
import pygame
from pygame.locals import *

BOARD_WIDTH = 7
BOARD_HEIGHT = 6

DIFFICULTY = 2  # how many moves to look ahead
SPACE_SIZE = 50  # size of the tokens and individual board spaces in pixels

FPS = 30
WINDOW_WIDTH, WINDOW_HEIGHT = 640, 480

X_MARGIN = (WINDOW_WIDTH - (BOARD_WIDTH * SPACE_SIZE)) // 2
Y_MARGIN = (WINDOW_HEIGHT - (BOARD_HEIGHT * SPACE_SIZE)) // 2

BRIGHTBLUE = (0, 50, 255)
WHITE = (255, 255, 255)

BGCOLOR = BRIGHTBLUE
TEXTCOLOR = WHITE

RED = 'red'
BLACK = 'black'
HUMAN = 'human'
COMPUTER = 'computer'
EMPTY = None


def get_new_board():
    board = []
    for x in range(BOARD_WIDTH):
        board.append([EMPTY] * BOARD_HEIGHT)
    return board
    # return [[EMPTY] * BOARD_HEIGHT] * BOARD_WIDTH


def is_valid_move(board, column):
    return 0 <= column < BOARD_WIDTH and board[column][0] == EMPTY


def get_lowest_empty_space(board, column):
    # for y in range(BOARD_HEIGHT - 1, -1, -1):
    #     if board[column][y] == EMPTY:
    #         return y
    # return -1
    y = BOARD_HEIGHT - 1
    while board[column][y] != EMPTY and y > 0:
        y -= 1
    return y


def draw_board(board, extra_token=None):
    # print('in draw_board')
    DISPLAY_SURFACE.fill(BGCOLOR)

    space_rect = pygame.Rect(0, 0, SPACE_SIZE, SPACE_SIZE)
    for x in range(BOARD_WIDTH):
        for y in range(BOARD_HEIGHT):
            space_rect.topleft = (X_MARGIN + (x * SPACE_SIZE), Y_MARGIN + (y * SPACE_SIZE))
            if board[x][y] == RED:
                DISPLAY_SURFACE.blit(RED_TOKEN_IMAGE, space_rect)
            elif board[x][y] == BLACK:
                DISPLAY_SURFACE.blit(BLACK_TOKEN_IMAGE, space_rect)

    # Draw the extra token
    if extra_token is not None:
        rect_for_extra_token = (extra_token['x'], extra_token['y'], SPACE_SIZE, SPACE_SIZE)
        if extra_token['color'] == RED:
            DISPLAY_SURFACE.blit(RED_TOKEN_IMAGE, rect_for_extra_token)
        elif extra_token['color'] == BLACK:
            DISPLAY_SURFACE.blit(BLACK_TOKEN_IMAGE, rect_for_extra_token)

    # draw board over the tokens
    for x in range(BOARD_WIDTH):
        for y in range(BOARD_HEIGHT):
            space_rect.topleft = (X_MARGIN + (x * SPACE_SIZE), Y_MARGIN + (y * SPACE_SIZE))
            DISPLAY_SURFACE.blit(BOARD_IMAGE, space_rect)

    # draw the red and black tokens off to the side
    DISPLAY_SURFACE.blit(RED_TOKEN_IMAGE, RED_PILE_RECT)        # red on the left
    DISPLAY_SURFACE.blit(BLACK_TOKEN_IMAGE, BLACK_PILE_RECT)    # black on the right


def animate_dropping_token(board, column, color):
    x = X_MARGIN + column * SPACE_SIZE
    y = Y_MARGIN - SPACE_SIZE
    drop_speed = 1.0
    lowest_empty_space = get_lowest_empty_space(board, column)

    while True:
        y += int(drop_speed)
        if (y - Y_MARGIN) // SPACE_SIZE >= lowest_empty_space:
            return
        draw_board(board, {'x': x, 'y': y, 'color': color})
        pygame.display.update()
        FPS_CLOCK.tick()


def get_human_move(board, show_help):
    print('in get_human_move')
    dragging_token = False
    token_x, token_y = None, None

    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                print('Exiting')
                pygame.quit()
                sys.exit(2)
            elif event.type == MOUSEBUTTONDOWN and not dragging_token and RED_PILE_RECT.collidepoint(event.pos):
                # print('Case 2')
                dragging_token = True
                token_x, token_y = event.pos
            elif event.type == MOUSEMOTION and dragging_token:
                # print('Case 3')
                token_x, token_y = event.pos
            elif event.type == MOUSEBUTTONUP and dragging_token:
                if token_y < Y_MARGIN and X_MARGIN < token_x < WINDOW_WIDTH - X_MARGIN:
                    column = (token_x - X_MARGIN) // SPACE_SIZE
                    if is_valid_move(board, column):
                        # print('Is valid move')
                        animate_dropping_token(board, column, RED)
                        # print('column =', column, 'lowest_empty_space =', get_lowest_empty_space(board, column))
                        board[column][get_lowest_empty_space(board, column)] = RED
                        draw_board(board)
                        pygame.display.update()
                        return
                token_x, token_y = None, None
                dragging_token = False

        if token_x is not None and token_y is not None:
            draw_board(board, {'x':token_x - SPACE_SIZE // 2, 'y':token_y - SPACE_SIZE // 2, 'color':RED})
        else:
            draw_board(board)

        if show_help:
            DISPLAY_SURFACE.blit(ARROW_IMG, ARROW_RECT)

        pygame.display.update()
        FPS_CLOCK.tick()


def is_winner(board, RED):
    # Horizontal
    for x in range(BOARD_WIDTH-3):
        for y in range(BOARD_HEIGHT):
            if board[x][y] == board[x+1][y] == board[x+2][y] == board[x+3][y] == RED:
                return True
    # Vertical
    for x in range(BOARD_WIDTH):
        for y in range(BOARD_HEIGHT-3):
            if board[x][y] == board[x][y+1] == board[x][y+2] == board[x][y+3] == RED:
                return True
    # Diagonal /
    for x in range(BOARD_WIDTH-3):
        for y in range(3, BOARD_HEIGHT):
            if board[x][y] == board[x+1][y-1] == board[x+2][y-2] == board[x+3][y-3] == RED:
                return True
    # Diagonal \
    for x in range(BOARD_WIDTH-3):
        for y in range(BOARD_HEIGHT-3):
            if board[x][y] == board[x+1][y+1] == board[x+2][y+2] == board[x+3][y+3] == RED:
                return True
    return False


def is_board_full(board):
    for row in board:
        if EMPTY in row:
            return False
    return True


def make_move(board, player, column):
    lowest = get_lowest_empty_space(board, column)
    if lowest != -1:
        board[column][lowest] = player


def get_potential_moves(board, tile, look_ahead):
    # print('is_board_full  -->', is_board_full(board))
    if look_ahead == 0 or is_board_full(board):
        return [0]*BOARD_WIDTH
    enemy_tile = RED if tile == BLACK else BLACK

    potential_moves = [0] * BOARD_WIDTH
    for first_move in range(BOARD_WIDTH):
        dupe_board = copy.deepcopy(board)
        if not is_valid_move(dupe_board, first_move):
            continue
        make_move(dupe_board, tile, first_move)
        if is_winner(board, tile):
            potential_moves[first_move] = 1     # Already won here. So break here
            break
        else:   # Calculate opponent's moves and determine the best one
            if is_board_full(dupe_board):
                potential_moves[first_move] = 0
            else:
                for counter_move in range(BOARD_WIDTH):
                    dupe_board2 = copy.deepcopy(dupe_board)
                    if not is_valid_move(dupe_board2, counter_move):
                        continue
                    make_move(dupe_board2, enemy_tile, counter_move)
                    if is_winner(dupe_board2, enemy_tile):
                        potential_moves[first_move] = -1    # Worst possible move
                        break
                    else:
                        results = get_potential_moves(dupe_board2, tile, look_ahead-1)
                        potential_moves[first_move] += (sum(results) / BOARD_WIDTH) / BOARD_WIDTH
    return potential_moves


def get_computer_move(board):
    potential_moves = get_potential_moves(board, BLACK, DIFFICULTY)
    print('potential_moves = ', potential_moves)
    best_move_fitness = -1
    valid_moves_columns_fitnesses = [potential_moves[i] for i in range(BOARD_WIDTH) if is_valid_move(board, i)]
    best_move_fitness = max(valid_moves_columns_fitnesses)
    best_moves = [i for i in range(len(potential_moves)) if potential_moves[i] == best_move_fitness]
    return random.choice(best_moves)


def animate_computer_move(board, column):
    x, y = BLACK_PILE_RECT.top, BLACK_PILE_RECT.left
    speed = 1.0
    # Move black tile up
    while y > Y_MARGIN - SPACE_SIZE:
        y -= int(speed)
        speed += 0.5
        draw_board(board, {'x': x, 'y': y, 'color': BLACK})
        pygame.display.update()
        FPS_CLOCK.tick()
    y = Y_MARGIN - SPACE_SIZE
    speed = 1.0
    while x > (X_MARGIN + column * SPACE_SIZE):
        x -= int(speed)
        speed += 0.5
        draw_board(board, {'x': x, 'y': y, 'color': BLACK})
        pygame.display.update()
        FPS_CLOCK.tick()
    animate_dropping_token(board, column, BLACK)


def run_game(is_first_game):
    print('In run game')
    if is_first_game:
        # Show the player how to move pieces
        turn = COMPUTER
        show_help = True
    else:
        if random.randint(0, 1):
            turn = COMPUTER
        else:
            turn = HUMAN
        show_help = False

    turn = HUMAN
    print('turn is', turn)
    main_board = get_new_board()

    while True:
        if turn == HUMAN:
            print('Getting Human move')
            get_human_move(main_board, show_help)
            if show_help:
                show_help = False
            if is_winner(main_board, RED):
                winner_image = HUMAN_WINNER_IMG
                break
            turn = COMPUTER
        else:
            print('Getting Computer move')
            column = get_computer_move(main_board)
            animate_computer_move(main_board, column)
            make_move(main_board, BLACK, column)
            if is_winner(main_board, BLACK):
                winner_image = COMPUTER_WINNER_IMG
                break
            turn = HUMAN

        if is_board_full(main_board):
            winner_image = TIE_WINNER_IMG

    while True:
        draw_board(main_board)
        DISPLAY_SURFACE.blit(winner_image, WINNER_RECT)
        pygame.display.update()
        FPS_CLOCK.tick()

        for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYUP and event.key == K_ESCAPE):
                pygame.quit()
                sys.exit()
            elif event.type == MOUSEBUTTONUP:
                return


def connect_four():
    global FPS_CLOCK, DISPLAY_SURFACE, RED_PILE_RECT, BLACK_PILE_RECT, RED_TOKEN_IMAGE, BLACK_TOKEN_IMAGE, BOARD_IMAGE, \
        HUMAN_WINNER_IMG, COMPUTER_WINNER_IMG, WINNER_RECT, ARROW_IMG, ARROW_RECT, TIE_WINNER_IMG, COMPUTER_WINNER_IMG

    pygame.init()
    FPS_CLOCK = pygame.time.Clock()
    DISPLAY_SURFACE = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    pygame.display.set_caption('4 in a row')

    RED_PILE_RECT = pygame.Rect(SPACE_SIZE // 2, WINDOW_HEIGHT - (3 * SPACE_SIZE // 2), SPACE_SIZE, SPACE_SIZE)
    BLACK_PILE_RECT = pygame.Rect(WINDOW_WIDTH - (3 * SPACE_SIZE // 2), WINDOW_WIDTH - (3 * SPACE_SIZE // 2),
                                  SPACE_SIZE, SPACE_SIZE)

    print(RED_PILE_RECT.x, RED_PILE_RECT.y, RED_PILE_RECT.h, RED_PILE_RECT.w)
    print(BLACK_PILE_RECT.x, BLACK_PILE_RECT.y, BLACK_PILE_RECT.h, BLACK_PILE_RECT.w)

    RED_TOKEN_IMAGE = pygame.image.load('/home/saibharadwaj/Downloads/Ast/Books/Python/makinggames/4row_red.png')
    RED_TOKEN_IMAGE = pygame.transform.smoothscale(RED_TOKEN_IMAGE, (SPACE_SIZE, SPACE_SIZE))
    BLACK_TOKEN_IMAGE = pygame.image.load('/home/saibharadwaj/Downloads/Ast/Books/Python/makinggames/4row_black.png')
    BLACK_TOKEN_IMAGE = pygame.transform.smoothscale(BLACK_TOKEN_IMAGE, (SPACE_SIZE, SPACE_SIZE))
    BOARD_IMAGE = pygame.image.load('/home/saibharadwaj/Downloads/Ast/Books/Python/makinggames/4row_board.png')
    BOARD_IMAGE = pygame.transform.smoothscale(BOARD_IMAGE, (SPACE_SIZE, SPACE_SIZE))

    HUMAN_WINNER_IMG = pygame.image.load(
        '/home/saibharadwaj/Downloads/Ast/Books/Python/makinggames/4row_humanwinner.png')
    COMPUTER_WINNER_IMG = pygame.image.load(
        '/home/saibharadwaj/Downloads/Ast/Books/Python/makinggames/4row_computerwinner.png')
    TIE_WINNER_IMG = pygame.image.load('/home/saibharadwaj/Downloads/Ast/Books/Python/makinggames/4row_tie.png')
    WINNER_RECT = HUMAN_WINNER_IMG.get_rect()
    WINNER_RECT.center = (WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2)

    ARROW_IMG = pygame.image.load('/home/saibharadwaj/Downloads/Ast/Books/Python/makinggames/4row_arrow.png')
    ARROW_RECT = ARROW_IMG.get_rect()
    ARROW_RECT.left = RED_PILE_RECT.right + 10
    ARROW_RECT.centery = RED_PILE_RECT.centery

    is_first_game = True

    while True:
        run_game(is_first_game)
        is_first_game = False


if __name__ == '__main__':
    connect_four()
