import pygame
from pygame.locals import *
import sys

BOARD_WIDTH = 7
BOARD_HEIGHT = 6

DIFFICULTY = 2
SPACE_SIZE = 50

FPS = 30
WINDOW_WIDTH, WINDOW_HEIGHT = 640, 480  # 480, 480

X_MARGIN = (WINDOW_WIDTH - (BOARD_WIDTH * SPACE_SIZE)) // 2
Y_MARGIN = (WINDOW_HEIGHT - (BOARD_HEIGHT * SPACE_SIZE)) // 2

# X_MARGIN = 50
# Y_MARGIN = 50

WHITE = (255, 255, 255)
BRIGHTBLUE = (0, 50, 255)
GREEN = (0, 255, 255)
DARK_GREEN = (0, 255, 0)
LIGHT_BLUE = (0, 0, 128)
BLACK = (0, 0, 0)
BGCOLOR = WHITE
LINE_COLOR = BLACK

RED = 'red'
BLACK = 'black'
HUMAN1 = 'human1'
HUMAN2 = 'human2'
COMPUTER = 'computer'
EMPTY = None


def get_new_board():
    board = [[EMPTY for _ in range(3)] for __ in range(3)]
    return board


def draw_board(board, extra_token=None):
    DISPLAY_SURFACE.fill(BGCOLOR)
    # print(pygame.mouse.get_pos())
    p1 = (X_MARGIN, Y_MARGIN)  # TOP LEFT
    p3 = (WINDOW_WIDTH - (X_MARGIN), Y_MARGIN)  # # TOP RIGHT
    p9 = (WINDOW_WIDTH - (X_MARGIN), WINDOW_HEIGHT - (Y_MARGIN))  # BOTTOM RIGHT
    p7 = (X_MARGIN, WINDOW_HEIGHT - (Y_MARGIN))  # BOTTOM LEFT

    p2 = tuple(((v1 + v2) // 2 for v1, v2 in zip(p1, p3)))
    p4 = tuple(((v1 + v2) // 2 for v1, v2 in zip(p1, p7)))
    p6 = tuple(((v1 + v2) // 2 for v1, v2 in zip(p3, p9)))
    p8 = tuple(((v1 + v2) // 2 for v1, v2 in zip(p7, p9)))

    p5 = ((p2[0] + p8[0]) // 2, (p4[1] + p6[1]) // 2)

    board_coords = [[p1, p2, p3], [p4, p5, p6], [p7, p8, p9]]
    global BOARD_COORDS, RED_MOVE_COUNT, BLACK_MOVE_COUNT, STAGE
    BOARD_COORDS = board_coords
    # print('board_coords are', board_coords)
    """ 
    (50, 50), 		(240, 50), 		(430, 50), 
    (50, 240)		(240, 240)		(430, 240), 
    (50, 430)		(240, 430)		(430, 430), 
    """
    pygame.draw.line(DISPLAY_SURFACE, LINE_COLOR, p1, p3, 5)  # --
    pygame.draw.line(DISPLAY_SURFACE, LINE_COLOR, p3, p9, 5)  # --|
    pygame.draw.line(DISPLAY_SURFACE, LINE_COLOR, p9, p7, 5)  # --|--
    pygame.draw.line(DISPLAY_SURFACE, LINE_COLOR, p7, p1, 5)  # --|--|

    pygame.draw.line(DISPLAY_SURFACE, LINE_COLOR, p2, p8, 5)  # -|-
    pygame.draw.line(DISPLAY_SURFACE, LINE_COLOR, p4, p6, 5)  # |-|
    pygame.draw.line(DISPLAY_SURFACE, LINE_COLOR, p1, p9, 5)  # \
    pygame.draw.line(DISPLAY_SURFACE, LINE_COLOR, p3, p7, 5)  # /

    # # Draw RED and BLACK tokens at the present locations
    # Draw circles at each point for reference
    for r in range(len(BOARD_COORDS)):
        for c in range(len(BOARD_COORDS[r])):
            point_x, point_y = BOARD_COORDS[r][c]
            existing_token_rect = pygame.Rect(point_x - SPACE_SIZE // 2, point_y - SPACE_SIZE // 2, SPACE_SIZE,
                                              SPACE_SIZE)
            pygame.draw.circle(DISPLAY_SURFACE, GREEN, BOARD_COORDS[r][c], SPACE_SIZE // 2, 3)
            if board[r][c] == RED:
                DISPLAY_SURFACE.blit(RED_TOKEN_IMAGE, existing_token_rect)
            elif board[r][c] == BLACK:
                DISPLAY_SURFACE.blit(BLACK_TOKEN_IMAGE, existing_token_rect)

    # Place the token in the mouse coords
    if extra_token:
        rect_for_extra_token = (extra_token['x'], extra_token['y'], SPACE_SIZE, SPACE_SIZE)
        if extra_token['color'] == RED:
            DISPLAY_SURFACE.blit(RED_TOKEN_IMAGE, rect_for_extra_token)
        elif extra_token['color'] == BLACK:
            DISPLAY_SURFACE.blit(BLACK_TOKEN_IMAGE, rect_for_extra_token)

    if STAGE == 1:
        DISPLAY_SURFACE.blit(RED_TOKEN_IMAGE, RED_PILE_RECT)  # red on the left
        DISPLAY_SURFACE.blit(BLACK_TOKEN_IMAGE, BLACK_PILE_RECT)  # black on the right
        move_count_font = pygame.font.Font('freesansbold.ttf', 10)
        red_text = move_count_font.render('red_move_count = {}'.format(RED_MOVE_COUNT), True, DARK_GREEN, WHITE)
        black_text = move_count_font.render('black_move_count = {}'.format(BLACK_MOVE_COUNT), True, DARK_GREEN, WHITE)
        red_textRect = red_text.get_rect()
        br_x, br_y = RED_PILE_RECT.bottomright
        red_textRect.topleft = (br_x + (SPACE_SIZE // 5), br_y - (SPACE_SIZE // 3))
        black_textRect = black_text.get_rect()
        bb_x, bb_y = BLACK_PILE_RECT.bottomright
        black_textRect.topleft = (bb_x - (SPACE_SIZE * 3.25), bb_y - (SPACE_SIZE // 3))
        DISPLAY_SURFACE.blit(red_text, red_textRect)  # Red Move counter
        DISPLAY_SURFACE.blit(black_text, black_textRect)  # Black Move counter
    else:
        font = pygame.font.Font('freesansbold.ttf', 20)
        text = font.render('Stage 2 start', True, DARK_GREEN, WHITE)
        textRect = text.get_rect()
        a1, a2 = RED_PILE_RECT.left, RED_PILE_RECT.top
        b1, b2 = BLACK_PILE_RECT.left, BLACK_PILE_RECT.top
        textRect.center = ((a1 + b1) // 2, (a2 + b2) // 2)
        # DISPLAY_SURFACE.blit(text, textRect)


def is_valid_move(board, row, col):
    return board[row][col] == EMPTY


def is_mouse_on_token(board, event, token_color):
    if event.type == 1:
        return False, -1, -1
    global stage2_row, stage2_col
    pos = event.pos
    for row in range(len(BOARD_COORDS)):
        for col in range(len(BOARD_COORDS[row])):
            cur_point_x, cur_point_y = BOARD_COORDS[row][col]
            if abs(pos[0] - cur_point_x) <= SPACE_SIZE and abs(pos[1] - cur_point_y) <= SPACE_SIZE and \
                    board[row][col] == token_color:
                print('Mouse over {} token at row = {} and col = {}'.format(board[row][col], row, col))
                return True, row, col
                # mouse_on_token = True
                # stage2_row, stage2_col = row, col
    return False, -1, -1


def get_human_move(board, token_color):
    print('In get_human_move for player', token_color, ' stage =', STAGE)
    token_x, token_y = None, None
    dragging_token = False
    token_moved = False

    player_token_rect = RED_PILE_RECT if token_color == RED else BLACK_PILE_RECT

    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                print('Exiting')
                pygame.quit()
                sys.exit(2)
            if STAGE == 1:
                if event.type == MOUSEBUTTONDOWN and not dragging_token and player_token_rect.collidepoint(event.pos):
                    dragging_token = True
                    token_x, token_y = event.pos
                elif event.type == MOUSEMOTION and dragging_token:
                    token_x, token_y = event.pos
                elif event.type == MOUSEBUTTONUP and dragging_token:
                    for row in range(len(BOARD_COORDS)):  # Find the circle which intersects with our token
                        for col in range(len(BOARD_COORDS[row])):
                            cur_point_x, cur_point_y = BOARD_COORDS[row][col]
                            if abs(event.pos[0] - cur_point_x) <= SPACE_SIZE and abs(
                                    event.pos[1] - cur_point_y) <= SPACE_SIZE:
                                if is_valid_move(board, row, col):
                                    board[row][col] = token_color
                                    draw_board(board)
                                    pygame.display.update()
                                    return
                                else:
                                    print('Invalid move')
                            token_x, token_y = None, None
                            dragging_token = False

            if STAGE == 2:
                # print('Getting movement for stage 2')
                print(event)
                mouse_on_token_flag, stage2_row, stage2_col = is_mouse_on_token(board, event, token_color)
                # print('mouse_on_token_flag, stage2_row, stage2_col are', mouse_on_token_flag, stage2_row, stage2_col)
                if event.type == MOUSEBUTTONDOWN and not dragging_token and mouse_on_token_flag:
                    dragging_token = True
                    token_x, token_y = event.pos
                elif event.type == MOUSEMOTION and dragging_token and mouse_on_token_flag:
                    board[stage2_row][stage2_col] = EMPTY
                    token_x, token_y = event.pos
                elif event.type == MOUSEBUTTONUP and dragging_token:
                    for row in range(len(BOARD_COORDS)):  # Find the circle which intersects with our token
                        for col in range(len(BOARD_COORDS[row])):
                            cur_point_x, cur_point_y = BOARD_COORDS[row][col]
                            if abs(event.pos[0] - cur_point_x) <= SPACE_SIZE and abs(
                                    event.pos[1] - cur_point_y) <= SPACE_SIZE:
                                if is_valid_move(board, row, col):
                                    # board[stage2_row][stage2_col] = token_color
                                    board[row][col] = token_color
                                    draw_board(board)
                                    pygame.display.update()
                                    return
                                else:
                                    print('Invalid move')
                                    # board[stage2_row][stage2_col] = token_color
                            token_x, token_y = None, None
                            dragging_token = False
                # if not token_moved:
                #     get_human_move(board, token_color)

        if token_x is not None and token_y is not None:
            draw_board(board, {'x': token_x - SPACE_SIZE // 2, 'y': token_y - SPACE_SIZE // 2, 'color': token_color})
        else:
            draw_board(board)

        pygame.display.update()
        FPS_CLOCK.tick()


def is_winner(board, token_color):
    if all(token == token_color for token in board[0]) or all(token == token_color for token in board[1]) or \
            all(token == token_color for token in board[2]):
        return True
    if all(row[0] == token_color for row in board) or all(row[1] == token_color for row in board) or \
            all(row[2] == token_color for row in board):
        return True
    if board[0][0] == board[1][1] == board[2][2] == token_color:
        return True
    if board[0][2] == board[1][1] == board[2][0] == token_color:
        return True
    return False


def run_game():
    global RED_MOVE_COUNT, BLACK_MOVE_COUNT, STAGE
    turn = HUMAN1
    board = get_new_board()

    while True:
        STAGE = 2 if BLACK_MOVE_COUNT >= 3 else 1
        # STAGE = 2
        # board[0][2] = board[1][2] = board[0][0] = RED
        # board[1][1] = board[1][0] = board[0][1] = BLACK
        # print('board =', board)
        # draw_board(board)
        if turn == HUMAN1:
            get_human_move(board, RED)
            RED_MOVE_COUNT += 1
            if is_winner(board, RED):
                print('RED WINS')
                break
            turn = HUMAN2
        else:
            get_human_move(board, BLACK)
            if is_winner(board, BLACK):
                print('BLACK WINS')
                break
            BLACK_MOVE_COUNT += 1
            turn = HUMAN1

    while True:
        draw_board(board)
        # DISPLAY_SURFACE.blit(winner_image, WINNER_RECT)
        # pygame.display.update()
        FPS_CLOCK.tick()

        for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYUP and event.key == K_ESCAPE):
                pygame.quit()
                sys.exit()
            elif event.type == MOUSEBUTTONUP:
                return


def dhaadi():
    global FPS_CLOCK, DISPLAY_SURFACE, RED_PILE_RECT, BLACK_PILE_RECT, RED_TOKEN_IMAGE, BLACK_TOKEN_IMAGE, BOARD_IMAGE, \
        COMPUTER_WINNER_IMG, WINNER_RECT, ARROW_IMG, ARROW_RECT, TIE_WINNER_IMG, HUMAN1_WINNER_IMG, HUMAN2_WINNER_IMG, \
        BOARD_COORDS, RED_MOVE_COUNT, BLACK_MOVE_COUNT, STAGE
    global stage2_row, stage2_col, mouse_on_token
    mouse_on_token = False
    pygame.init()
    FPS_CLOCK = pygame.time.Clock()
    DISPLAY_SURFACE = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    pygame.display.set_caption('DHAADI')

    RED_MOVE_COUNT, BLACK_MOVE_COUNT = 0, 0
    STAGE = 'stage_1'

    RED_PILE_RECT = pygame.Rect(SPACE_SIZE // 2, WINDOW_HEIGHT - (3 * SPACE_SIZE // 2), SPACE_SIZE, SPACE_SIZE)
    BLACK_PILE_RECT = pygame.Rect(WINDOW_WIDTH - (3 * SPACE_SIZE // 2), WINDOW_HEIGHT - (3 * SPACE_SIZE // 2),
                                  SPACE_SIZE, SPACE_SIZE)

    # abc = RED_PILE_RECT.topleft

    images_location = ''
    RED_TOKEN_IMAGE = pygame.image.load(images_location + 'red.png')
    BLACK_TOKEN_IMAGE = pygame.image.load(images_location + 'black.png')
    RED_TOKEN_IMAGE = pygame.transform.smoothscale(RED_TOKEN_IMAGE, (SPACE_SIZE, SPACE_SIZE))
    BLACK_TOKEN_IMAGE = pygame.transform.smoothscale(BLACK_TOKEN_IMAGE, (SPACE_SIZE, SPACE_SIZE))

    # HUMAN1_WINNER_IMG = pygame.image.load(images_location+'4row_humanwinner.png')
    # HUMAN2_WINNER_IMG = pygame.image.load(images_location+'4row_humanwinner.png')
    # COMPUTER_WINNER_IMG = pygame.image.load(images_location+'4row_computerwinner.png')
    # TIE_WINNER_IMG = pygame.image.load(images_location+'4row_tie.png')
    # WINNER_RECT = HUMAN1_WINNER_IMG.get_rect()
    # WINNER_RECT.center = (WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2)

    while True:
        run_game()

        for event in pygame.event.get():
            if event.type == QUIT:
                print('Exiting')
                pygame.quit()
                sys.exit(2)

    pass


if __name__ == '__main__':
    dhaadi()
