import pygame
from pygame.locals import *
import sys

BOARD_WIDTH = 7
BOARD_HEIGHT = 6

DIFFICULTY = 2
SPACE_SIZE = 50

FPS = 30
WINDOW_WIDTH, WINDOW_HEIGHT = 640, 480 #480, 480

X_MARGIN = (WINDOW_WIDTH - (BOARD_WIDTH * SPACE_SIZE)) // 2
Y_MARGIN = (WINDOW_HEIGHT - (BOARD_HEIGHT * SPACE_SIZE)) // 2

# X_MARGIN = 50
# Y_MARGIN = 50

WHITE = (255, 255, 255)
BRIGHTBLUE = (0, 50, 255)
GREEN = (0, 255, 255)
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
    DISPLAY_SURFACE.fill(BRIGHTBLUE)
    # print(pygame.mouse.get_pos())
    p1 = (X_MARGIN, Y_MARGIN)   # TOP LEFT
    p3 = (WINDOW_WIDTH-(X_MARGIN), Y_MARGIN)    # # TOP RIGHT
    p9 = (WINDOW_WIDTH-(X_MARGIN), WINDOW_HEIGHT-(Y_MARGIN))    # BOTTOM RIGHT
    p7 = (X_MARGIN, WINDOW_HEIGHT-(Y_MARGIN))   # BOTTOM LEFT

    p2 = tuple(((v1+v2) // 2 for v1, v2 in zip(p1, p3)))
    p4 = tuple(((v1+v2) // 2 for v1, v2 in zip(p1, p7)))
    p6 = tuple(((v1+v2) // 2 for v1, v2 in zip(p3, p9)))
    p8 = tuple(((v1+v2) // 2 for v1, v2 in zip(p7, p9)))

    p5 = ((p2[0]+p8[0])//2, (p4[1]+p6[1])//2)

    board_coords = [[p1, p2, p3], [p4, p5, p6], [p7, p8, p9]]
    global BOARD_COORDS
    BOARD_COORDS = board_coords
    # print('board_coords are', board_coords)
    """ 
    (50, 50), 		(240, 50), 		(430, 50), 
    (50, 240)		(240, 240)		(430, 240), 
    (50, 430)		(240, 430)		(430, 430), 
    """
    pygame.draw.line(DISPLAY_SURFACE, LINE_COLOR, p1, p3, 5)    # --
    pygame.draw.line(DISPLAY_SURFACE, LINE_COLOR, p3, p9, 5)    # --|
    pygame.draw.line(DISPLAY_SURFACE, LINE_COLOR, p9, p7, 5)    # --|--
    pygame.draw.line(DISPLAY_SURFACE, LINE_COLOR, p7, p1, 5)    # --|--|

    pygame.draw.line(DISPLAY_SURFACE, LINE_COLOR, p2, p8, 5)    # -|-
    pygame.draw.line(DISPLAY_SURFACE, LINE_COLOR, p4, p6, 5)    # |-|
    pygame.draw.line(DISPLAY_SURFACE, LINE_COLOR, p1, p9, 5)    # \
    pygame.draw.line(DISPLAY_SURFACE, LINE_COLOR, p3, p7, 5)    # /

    # # Draw RED and BLACK tokens at the present locations
    # Draw circles at each point for reference
    for r in range(len(BOARD_COORDS)):
        for c in range(len(BOARD_COORDS[r])):
            point_x, point_y = BOARD_COORDS[r][c]
            existing_token_rect = pygame.Rect(point_x-SPACE_SIZE // 2, point_y-SPACE_SIZE // 2, SPACE_SIZE, SPACE_SIZE)
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

    DISPLAY_SURFACE.blit(RED_TOKEN_IMAGE, RED_PILE_RECT)  # red on the left
    DISPLAY_SURFACE.blit(BLACK_TOKEN_IMAGE, BLACK_PILE_RECT)  # black on the right


def get_human_move(board, token_color):
    print('In get_human_move for player', token_color)
    token_x, token_y = None, None
    dragging_token = False

    player_token_rect = RED_PILE_RECT if token_color == RED else BLACK_PILE_RECT

    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                print('Exiting')
                pygame.quit()
                sys.exit(2)
            elif event.type == MOUSEBUTTONDOWN and not dragging_token and player_token_rect.collidepoint(event.pos):
                dragging_token = True
                token_x, token_y = event.pos
            elif event.type == MOUSEMOTION and dragging_token:
                token_x, token_y = event.pos
            elif event.type == MOUSEBUTTONUP and dragging_token:
                # Find the circle which intersects with our token
                for row in range(len(BOARD_COORDS)):
                    for col in range(len(BOARD_COORDS[row])):
                        cur_point_x, cur_point_y = BOARD_COORDS[row][col]
                        if abs(event.pos[0] - cur_point_x) <= SPACE_SIZE and abs(event.pos[1] - cur_point_y) <= SPACE_SIZE:
                            print('Point collide at row {}, column {}'.format(row, col))
                            board[row][col] = token_color
                            print('board =', board)
                            draw_board(board)
                            pygame.display.update()
                            return
                        token_x, token_y = None, None
                        dragging_token = False

        if token_x is not None and token_y is not None:
            draw_board(board, {'x':token_x - SPACE_SIZE // 2, 'y':token_y - SPACE_SIZE // 2, 'color':token_color})
        else:
            draw_board(board)

        pygame.display.update()
        FPS_CLOCK.tick()


def run_game(is_first_game):
    turn = HUMAN1
    board = get_new_board()
    
    while True:
        if turn == HUMAN1:
            get_human_move(board, RED)
            turn = HUMAN2
        else:
            get_human_move(board, BLACK)
            turn = HUMAN1
    
    # draw_board(board)
    #
    # pygame.display.update()
    # FPS_CLOCK.tick()
    return


def dhaadi():
    global FPS_CLOCK, DISPLAY_SURFACE, RED_PILE_RECT, BLACK_PILE_RECT, RED_TOKEN_IMAGE, BLACK_TOKEN_IMAGE, BOARD_IMAGE, \
        COMPUTER_WINNER_IMG, WINNER_RECT, ARROW_IMG, ARROW_RECT, TIE_WINNER_IMG, HUMAN1_WINNER_IMG, HUMAN2_WINNER_IMG, \
        BOARD_COORDS
    
    pygame.init()
    FPS_CLOCK = pygame.time.Clock()
    DISPLAY_SURFACE = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    pygame.display.set_caption('DHAADI')

    RED_PILE_RECT = pygame.Rect(SPACE_SIZE // 2, WINDOW_HEIGHT - (3 * SPACE_SIZE // 2), SPACE_SIZE, SPACE_SIZE)
    BLACK_PILE_RECT = pygame.Rect(WINDOW_WIDTH - (3*SPACE_SIZE//2), WINDOW_HEIGHT - (3 * SPACE_SIZE // 2), SPACE_SIZE, SPACE_SIZE)

    images_location = '/home/saibharadwaj/Downloads/Ast/Books/Python/makinggames/'
    RED_TOKEN_IMAGE = pygame.image.load(images_location+'4row_red.png')
    BLACK_TOKEN_IMAGE = pygame.image.load(images_location+'4row_black.png')
    RED_TOKEN_IMAGE = pygame.transform.smoothscale(RED_TOKEN_IMAGE, (SPACE_SIZE, SPACE_SIZE))
    BLACK_TOKEN_IMAGE = pygame.transform.smoothscale(BLACK_TOKEN_IMAGE, (SPACE_SIZE, SPACE_SIZE))

    HUMAN1_WINNER_IMG = pygame.image.load(images_location+'4row_humanwinner.png')
    HUMAN2_WINNER_IMG = pygame.image.load(images_location+'4row_humanwinner.png')
    COMPUTER_WINNER_IMG = pygame.image.load(images_location+'4row_computerwinner.png')
    TIE_WINNER_IMG = pygame.image.load(images_location+'4row_tie.png')
    WINNER_RECT = HUMAN1_WINNER_IMG.get_rect()
    WINNER_RECT.center = (WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2)

    is_first_game = True

    while True:
        run_game(is_first_game)
        is_first_game = False

        for event in pygame.event.get():
            if event.type == QUIT:
                print('Exiting')
                pygame.quit()
                sys.exit(2)

    
    pass


if __name__ == '__main__':
    dhaadi()





