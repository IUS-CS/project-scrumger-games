import pygame

from Util.window import Window

def text_ob(text, font, color):
    textforScreen = font.render(text, True, color)
    return textforScreen, textforScreen.get_rect()


def game_over():
    """"Create Game Over Screen"""
    WIN = Window.WIN
    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)

    end = True

    while end:
        for event in pygame.event.get():
            print(event)

            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        WIN.fill(BLACK)
        text = pygame.font.SysFont('Times New Roman', 100)
        Text, TextRect = text_ob("Game Over", text, WHITE)
        TextRect.center = ((Window.WIDTH / 2), (Window.HEIGHT / 2))
        WIN.blit(Text, TextRect)
        pygame.display.update()

