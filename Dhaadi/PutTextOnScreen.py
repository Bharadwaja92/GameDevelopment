import pygame

pygame.init()

white = (255, 255, 255)
green = (0, 255, 0)
blue = (0, 0, 128)

WINDOW_WIDTH, WINDOW_HEIGHT = 640, 480 #480, 480
SPACE_SIZE = 50
DISPLAY_SURFACE = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption('Text test')

font = pygame.font.Font('freesansbold.ttf', 10)
text = font.render('Move Counter', True, green, blue)

textRect = text.get_rect()
# br_x, br_y = 35, 375
br_x, br_y = 75, 455
textRect.topleft = (br_x - (SPACE_SIZE), br_y - (SPACE_SIZE))
# textRect.center = (WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2)

while True:
    DISPLAY_SURFACE.fill(white)
    DISPLAY_SURFACE.blit(text, textRect)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            import sys
            sys.exit(2)
    pygame.display.update()
