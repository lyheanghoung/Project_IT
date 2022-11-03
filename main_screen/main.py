import pygame, sys
from button import Button

pygame.init()

SCREEN = pygame.display.set_mode((1280, 720))
pygame.display.set_caption("Menu")

BG = pygame.image.load("assets/Background4.webp")
instruction1 = pygame.image.load("assets/1player.png")
instruction2 = pygame.image.load("assets/2player.png")

def get_font(size): # Returns Press-Start-2P in the desired size
    return pygame.font.Font("assets/8-BIT WONDER.TTF", size)

def play():
    while True:
        SCREEN.blit(BG, (0, 0))

        MENU_MOUSE_POS = pygame.mouse.get_pos()
        PLAY_MOUSE_POS = pygame.mouse.get_pos()

        MENU_TEXT = get_font(50).render("Please Choose Player", True, "#ff0000")
        MENU_RECT = MENU_TEXT.get_rect(center=(640, 120))

        PLAYER1_BUTTON = Button(image=pygame.image.load("assets/Instructions Rect.png"), pos=(640, 280), 
                            text_input="1 PLAYER", font=get_font(48), base_color="#ffda29", hovering_color="White")
        PLAYER2_BUTTON = Button(image=pygame.image.load("assets/Instructions Rect.png"), pos=(640, 460), 
                            text_input="2 PLAYERS", font=get_font(48), base_color="#ffDA29", hovering_color="White")
        
        SCREEN.blit(MENU_TEXT, MENU_RECT)

        PLAY_BACK = Button(image=None, pos=(640, 600), text_input="BACK", font=get_font(40), base_color="#ffda29", hovering_color="Green")

        PLAY_BACK.changeColor(PLAY_MOUSE_POS)
        PLAY_BACK.update(SCREEN)

        for button in [PLAYER1_BUTTON, PLAYER2_BUTTON]:
            button.changeColor(MENU_MOUSE_POS)
            button.update(SCREEN)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if PLAY_BACK.checkForInput(PLAY_MOUSE_POS):
                    main_menu()
        pygame.display.update()
    
def instructions():
    while True:
        INSTRUCTIONS_MOUSE_POS = pygame.mouse.get_pos()

        SCREEN.blit(BG, (0, 0))
        SCREEN.blit(instruction1, (130,180))
        SCREEN.blit(instruction2, (700, 180))
        INSTRUCTIONS_TEXT = get_font(60).render("How to Play Connect4", True, "#ff0000")
        INSTRUCTIONS_RECT = INSTRUCTIONS_TEXT.get_rect(center=(640, 90))
        SCREEN.blit(INSTRUCTIONS_TEXT, INSTRUCTIONS_RECT)

        INSTRUCTIONS_BACK = Button(image=None, pos=(640, 650), 
                            text_input="BACK", font=get_font(40), base_color="#ffda29", hovering_color="Green")

        INSTRUCTIONS_BACK.changeColor(INSTRUCTIONS_MOUSE_POS)
        INSTRUCTIONS_BACK.update(SCREEN)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if INSTRUCTIONS_BACK.checkForInput(INSTRUCTIONS_MOUSE_POS):
                    main_menu()

        pygame.display.update()

def main_menu():
    while True:
        SCREEN.blit(BG, (0, 0))

        MENU_MOUSE_POS = pygame.mouse.get_pos()

        MENU_TEXT = get_font(100).render("WELCOME", True, "#ff0000")
        MENU_RECT = MENU_TEXT.get_rect(center=(640, 100))

        PLAY_BUTTON = Button(image=pygame.image.load("assets/Instructions Rect.png"), pos=(640, 250), 
                            text_input="START GAME", font=get_font(48), base_color="#ffda29", hovering_color="White")
        INSTRUCTIONS_BUTTON = Button(image=pygame.image.load("assets/Instructions Rect.png"), pos=(640, 400), 
                            text_input="INSTRUCTIONS", font=get_font(48), base_color="#ffDA29", hovering_color="White")
        QUIT_BUTTON = Button(image=pygame.image.load("assets/Instructions Rect.png"), pos=(640, 550), 
                            text_input="QUIT GAME", font=get_font(48), base_color="#ffDA29", hovering_color="White")

        SCREEN.blit(MENU_TEXT, MENU_RECT)

        for button in [PLAY_BUTTON, INSTRUCTIONS_BUTTON, QUIT_BUTTON]:
            button.changeColor(MENU_MOUSE_POS)
            button.update(SCREEN)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if PLAY_BUTTON.checkForInput(MENU_MOUSE_POS):
                    play()
                if INSTRUCTIONS_BUTTON.checkForInput(MENU_MOUSE_POS):
                    instructions()
                if QUIT_BUTTON.checkForInput(MENU_MOUSE_POS):
                    pygame.quit()
                    sys.exit()

        pygame.display.update()

main_menu()