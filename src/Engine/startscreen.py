import pygame

from src.Util.window import Window


def text_ob(text, font, color):
    textforScreen = font.render(text, True, color)
    return textforScreen, textforScreen.get_rect()


def start_screen():
    """"Create Start Screen"""
    WIN = Window.WIN
    white = (255, 255, 255)
    black = (0, 0, 0)

    blue = pygame.Color(0,0, 255)
    aqua = pygame.Color(0, 255, 255)

    start = True
    click = pygame.mouse.get_pressed()

    while start:
        """"When mouse clicked end Start Screen"""
        for event in pygame.event.get():
            if event.type == click:
                print(click)
                start = False

        """"Fill in Start Screen with color and text"""
        WIN.fill(black)
        text = pygame.font.SysFont('Times New Roman', 100)
        Text, TextRect = text_ob("The Froggerithm", text, white)
        text2 = pygame.font.SysFont('Times New Roman', 35)
        Text2, TextRect2 = text_ob("Click on the Screen to Start the Game", text2, aqua)
        TextRect.center = ((Window.WIDTH/2), (Window.HEIGHT/2))
        TextRect2.center = (((Window.WIDTH)/2), ((Window.HEIGHT+200)/2))
        WIN.blit(Text, TextRect)
        WIN.blit(Text2, TextRect2)
        pygame.display.update()




