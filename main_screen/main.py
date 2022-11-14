import pygame
from button import Button
import numpy as np
import pygame
import sys
import random
import math

pygame.init()

SCREEN = pygame.display.set_mode((1000, 900))
pygame.display.set_caption("Connect4 Game")

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
        MENU_RECT = MENU_TEXT.get_rect(center=(500, 120))

        PLAYER1_BUTTON = Button(image=pygame.image.load("assets/Instructions Rect.png"), pos=(500, 300), 
                            text_input="1 PLAYER", font=get_font(48), base_color="#ffda29", hovering_color="White")
        PLAYER2_BUTTON = Button(image=pygame.image.load("assets/Instructions Rect.png"), pos=(500, 450), 
                            text_input="2 PLAYERS", font=get_font(48), base_color="#ffDA29", hovering_color="White")
        
        SCREEN.blit(MENU_TEXT, MENU_RECT)

        PLAY_BACK = Button(image=None, pos=(500, 620), text_input="BACK", font=get_font(50), base_color="#ffda29", hovering_color="Green")

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
                if PLAYER1_BUTTON.checkForInput(PLAY_MOUSE_POS):
                    rand = random.Random()
                    class Connect4():
                        NUM_ROWS = 8
                        NUM_COLS = 10
                        NUM2WIN = 4
                        def __init__(self):
                            self.board = np.zeros((self.NUM_ROWS, self.NUM_COLS))

                        def __str__(self):
                            str_board = "\n\n" + str(self.board).replace("0.", "_").replace("-1.", " O").replace("1.", "X")
                            str_board = str_board.replace("[", " ").replace("]", " ")
                            return str_board
                            
                        def get_avail_moves(self):
                            return [m for m in range(self.NUM_COLS) if self.board[0][m] == 0] # check top row for empty

                        def make_move(self, move):
                            if np.sum(self.board) == 0:
                                player = 1
                            else:
                                player = -1
                            
                            j = 0
                            while j+1 < self.NUM_ROWS and self.board[j+1][move] == 0: j+=1
                            
                            self.board[j][move] = player

                        def get_winner(self):
                            for i in range(self.NUM_ROWS-self.NUM2WIN+1):
                                for j in range(self.NUM_COLS-self.NUM2WIN+1):
                                    subboard = self.board[i:i+self.NUM2WIN, j:j+self.NUM2WIN]
                                    if np.max(np.abs(np.sum(subboard, 0))) == self.NUM2WIN:
                                        return True
                                    if np.max(np.abs(np.sum(subboard, 1))) == self.NUM2WIN:
                                        return True
                                    elif np.abs(sum([subboard[k, k] for k in range(self.NUM2WIN)])) == self.NUM2WIN: # diag
                                        return True
                                    elif np.abs(sum([subboard[k, self.NUM2WIN-1-k] for k in range(self.NUM2WIN)])) == self.NUM2WIN: # opp diag
                                        return True
                            return False


                    def main():
                        XO = {-1: "O", 0: "Nobody", 1: "X"}
                        my_game = Connect4()
                        moves = my_game.get_avail_moves()
                        print(my_game)
                        player = 1 # first player is always 1
                        human_player = rand.choice([1, -1])
                        while moves != []:

                            if player == human_player:
                                print(f"Available moves are: {moves}")
                                move = int(input("Enter move human: "))
                            else:
                                move = rand.choice(moves)
                            my_game.make_move(move)
                            print(my_game)
                            winner =  my_game.get_winner()
                            if winner:
                                print(f"{XO[player]} Wins!")
                                break
                            moves = my_game.get_avail_moves()
                            player = -player

                    class Connect4_GUI(Connect4):

                        BLUE = (0, 0, 255)
                        LIGHT_BLUE = (0, 0, 128)
                        BLACK = (0, 0, 0)
                        RED = (255, 0, 0)
                        YELLOW = (255, 255, 0)
                        # coin1 = pygame.image.load("assets/coin1.jpg")

                        SQUARESIZE = 100
                        WIDTH = Connect4.NUM_COLS*SQUARESIZE
                        HEIGHT = (1+Connect4.NUM_ROWS)*SQUARESIZE
                        SIZE = (WIDTH, HEIGHT)
                        RADIUS = int(SQUARESIZE/2 - 5)
                        SCREEN = pygame.display.set_mode(SIZE)

                        def draw_board(self):
                            for c in range(self.NUM_COLS):
                                for r in range(self.NUM_ROWS):
                                    loc_size = (c*self.SQUARESIZE, (r+1)*self.SQUARESIZE, self.SQUARESIZE, self.SQUARESIZE)
                                    pygame.draw.rect(self.SCREEN, self.BLUE, loc_size)
                                    loc = (int((c+0.5)*self.SQUARESIZE), int((r+1.5)*self.SQUARESIZE))
                                    pygame.draw.circle(self.SCREEN, self.BLACK, loc, self.RADIUS)
                            
                            for c in range(self.NUM_COLS):
                                for r in range(self.NUM_ROWS):		
                                    if self.board[r][c] == 1:
                                        loc = (int((c+0.5)*self.SQUARESIZE), int((r+1.5)*self.SQUARESIZE))
                                        pygame.draw.circle(self.SCREEN, self.RED, loc, self.RADIUS)
                                    elif self.board[r][c] == -1: 
                                        loc = (int((c+0.5)*self.SQUARESIZE), int((r+1.5)*self.SQUARESIZE))
                                        pygame.draw.circle(self.SCREEN, self.YELLOW, loc, self.RADIUS)
                            pygame.display.update()

                        def run_game(self):
                            pygame.init()
                            myfont = pygame.font.Font("assets/8-BIT WONDER.TTF", 50)
                            self.draw_board()
                            pygame.display.update()


                            moves = self.get_avail_moves()
                            player = 1 # first player is always 1
                            human_player = rand.choice([1, -1])
                            winner = False
                            exit_flag = False
                            while moves != [] and winner == False and exit_flag == False:
                                for event in pygame.event.get():
                                    if event.type == pygame.QUIT:
                                        exit_flag = True

                                    if event.type == pygame.MOUSEMOTION:
                                        pygame.draw.rect(self.SCREEN, self.BLACK, (0,0, self.WIDTH, self.SQUARESIZE))
                                        posx = event.pos[0]
                                        if player ==  1:
                                            pygame.draw.circle(self.SCREEN, self.RED, (posx, int(self.SQUARESIZE/2)), self.RADIUS)
                                        else: 
                                            pygame.draw.circle(self.SCREEN, self.YELLOW, (posx, int(self.SQUARESIZE/2)), self.RADIUS)
                                        
                                        pygame.display.update()

                                    # wait for player input
                                    if player == human_player and event.type == pygame.MOUSEBUTTONDOWN:
                                        pygame.draw.rect(self.SCREEN, self.BLACK, (0,0, self.WIDTH, self.SQUARESIZE))
                                        posx = event.pos[0]
                                        move = int(math.floor(posx/self.SQUARESIZE))
                                        if move in moves:
                                            self.make_move(move)
                                            self.draw_board()
                                            if self.get_winner():
                                                if human_player == 1:
                                                    label = myfont.render("Horayyy You Win", 1, self.RED)
                                                    # pygame.time.wait(3000)
                                                    # play()
                                                else:
                                                    label = myfont.render("Horayyy You Win", 1, self.YELLOW)
                                                    # pygame.time.wait(3000)
                                                    # play()
                                                self.SCREEN.blit(label, (40,10))
                                                self.draw_board()
                                                winner = True
                                                break
                                                
                                            player = -player

                                    # Ask for Player 2 Input
                                    elif player == -human_player:			
                                        move =  rand.choice(moves)
                                        if move in moves:
                                            self.make_move(move)
                                            self.draw_board()
                                            if self.get_winner():
                                                if player == 1:
                                                    label = myfont.render("Try Again You Lose", 1, self.coin1)
                                                    pygame.time.wait(3000)
                                                    play()
                                                else:
                                                    label = myfont.render("Try Again You Lose", 1, self.YELLOW)
                                                    # pygame.time.wait(3000)
                                                    # play()
                                                self.SCREEN.blit(label, (40,10))
                                                self.draw_board()
                                                winner = True
                                                break
                                                
                                            player = -player
                                moves = self.get_avail_moves()
                            if winner == False and moves == []:
                                label = myfont.render("It's a Draw :/", 1, self.LIGHT_BLUE)
                                self.SCREEN.blit(label, (40,10))
                                self.draw_board()
                            while exit_flag == False:
                                for event in pygame.event.get():
                                    if event.type == pygame.QUIT:
                                        exit_flag = True
                            pygame.quit()

                    def main():
                        my_game = Connect4_GUI()
                        my_game.run_game()

                    if __name__ == "__main__":
                        main()
                if PLAYER2_BUTTON.checkForInput(PLAY_MOUSE_POS):
                    BLUE = (0,0,255)
                    BLACK = (0,0,0)
                    RED = (255,0,0)
                    YELLOW = (255,255,0)

                    ROW_COUNT = 8
                    COLUMN_COUNT = 10

                    def create_board():
                        board = np.zeros((ROW_COUNT,COLUMN_COUNT))
                        return board

                    def drop_piece(board, row, col, piece):
                        board[row][col] = piece

                    def is_valid_location(board, col):
                        return board[ROW_COUNT-1][col] == 0

                    def get_next_open_row(board, col):
                        for r in range(ROW_COUNT):
                            if board[r][col] == 0:
                                return r

                    def print_board(board):
                        print(np.flip(board, 0))

                    def winning_move(board, piece):
                        # Check horizontal locations for win
                        for c in range(COLUMN_COUNT-3):
                            for r in range(ROW_COUNT):
                                if board[r][c] == piece and board[r][c+1] == piece and board[r][c+2] == piece and board[r][c+3] == piece:
                                    return True

                        # Check vertical locations for win
                        for c in range(COLUMN_COUNT):
                            for r in range(ROW_COUNT-3):
                                if board[r][c] == piece and board[r+1][c] == piece and board[r+2][c] == piece and board[r+3][c] == piece:
                                    return True

                        # Check positively sloped diaganols
                        for c in range(COLUMN_COUNT-3):
                            for r in range(ROW_COUNT-3):
                                if board[r][c] == piece and board[r+1][c+1] == piece and board[r+2][c+2] == piece and board[r+3][c+3] == piece:
                                    return True

                        # Check negatively sloped diaganols
                        for c in range(COLUMN_COUNT-3):
                            for r in range(3, ROW_COUNT):
                                if board[r][c] == piece and board[r-1][c+1] == piece and board[r-2][c+2] == piece and board[r-3][c+3] == piece:
                                    return True

                    def draw_board(board):
                        for c in range(COLUMN_COUNT):
                            for r in range(ROW_COUNT):
                                pygame.draw.rect(screen, BLUE, (c*SQUARESIZE, r*SQUARESIZE+SQUARESIZE, SQUARESIZE, SQUARESIZE))
                                pygame.draw.circle(screen, BLACK, (int(c*SQUARESIZE+SQUARESIZE/2), int(r*SQUARESIZE+SQUARESIZE+SQUARESIZE/2)), RADIUS)
                        
                        for c in range(COLUMN_COUNT):
                            for r in range(ROW_COUNT):		
                                if board[r][c] == 1:
                                    pygame.draw.circle(screen, RED, (int(c*SQUARESIZE+SQUARESIZE/2), height-int(r*SQUARESIZE+SQUARESIZE/2)), RADIUS)
                                elif board[r][c] == 2: 
                                    pygame.draw.circle(screen, YELLOW, (int(c*SQUARESIZE+SQUARESIZE/2), height-int(r*SQUARESIZE+SQUARESIZE/2)), RADIUS)
                        pygame.display.update()


                    board = create_board()
                    print_board(board)
                    game_over = False
                    turn = 0

                    pygame.init()

                    SQUARESIZE = 100

                    width = COLUMN_COUNT * SQUARESIZE
                    height = (ROW_COUNT+1) * SQUARESIZE

                    size = (width, height)

                    RADIUS = int(SQUARESIZE/2 - 5)

                    screen = pygame.display.set_mode(size)
                    draw_board(board)
                    pygame.display.update()

                    myfont = pygame.font.Font("assets/8-BIT WONDER.TTF", 50)

                    while not game_over:

                        for event in pygame.event.get():
                            if event.type == pygame.QUIT:
                                sys.exit()

                            if event.type == pygame.MOUSEMOTION:
                                pygame.draw.rect(screen, BLACK, (0,0, width, SQUARESIZE))
                                posx = event.pos[0]
                                if turn == 0:
                                    pygame.draw.circle(screen, RED, (posx, int(SQUARESIZE/2)), RADIUS)
                                else: 
                                    pygame.draw.circle(screen, YELLOW, (posx, int(SQUARESIZE/2)), RADIUS)
                            pygame.display.update()

                            if event.type == pygame.MOUSEBUTTONDOWN:
                                pygame.draw.rect(screen, BLACK, (0,0, width, SQUARESIZE))
                                #print(event.pos)
                                # Ask for Player 1 Input
                                if turn == 0:
                                    posx = event.pos[0]
                                    col = int(math.floor(posx/SQUARESIZE))

                                    if is_valid_location(board, col):
                                        row = get_next_open_row(board, col)
                                        drop_piece(board, row, col, 1)

                                        if winning_move(board, 1):
                                            label = myfont.render("Horayyy Player 1 wins", 1, RED)
                                            screen.blit(label, (40,10))
                                            game_over = True

                                # # Ask for Player 2 Input
                                else:				
                                    posx = event.pos[0]
                                    col = int(math.floor(posx/SQUARESIZE))

                                    if is_valid_location(board, col):
                                        row = get_next_open_row(board, col)
                                        drop_piece(board, row, col, 2)

                                        if winning_move(board, 2):
                                            label = myfont.render("Horayyy Player 2 wins", 1, YELLOW)
                                            screen.blit(label, (40,10))
                                            game_over = True

                                print_board(board)
                                draw_board(board)

                                turn += 1
                                turn = turn % 2

                                if game_over:
                                    pygame.time.wait(3000)
                                    play()
        pygame.display.update()
    
def instructions():
    while True:
        INSTRUCTIONS_MOUSE_POS = pygame.mouse.get_pos()

        SCREEN.blit(BG, (0, 0))
        SCREEN.blit(instruction1, (35,220))
        SCREEN.blit(instruction2, (520,220))
        INSTRUCTIONS_TEXT = get_font(50).render("How to Play Connect4", True, "#ff0000")
        INSTRUCTIONS_RECT = INSTRUCTIONS_TEXT.get_rect(center=(500, 100))
        SCREEN.blit(INSTRUCTIONS_TEXT, INSTRUCTIONS_RECT)

        INSTRUCTIONS_BACK = Button(image=None, pos=(500, 750), 
                            text_input="BACK", font=get_font(50), base_color="#ffda29", hovering_color="Green")

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
        MENU_RECT = MENU_TEXT.get_rect(center=(500, 150))

        PLAY_BUTTON = Button(image=pygame.image.load("assets/Instructions Rect.png"), pos=(500, 350), 
                            text_input="START GAME", font=get_font(48), base_color="#ffda29", hovering_color="White")
        INSTRUCTIONS_BUTTON = Button(image=pygame.image.load("assets/Instructions Rect.png"), pos=(500, 500), 
                            text_input="INSTRUCTIONS", font=get_font(48), base_color="#ffDA29", hovering_color="White")
        QUIT_BUTTON = Button(image=pygame.image.load("assets/Instructions Rect.png"), pos=(500, 650), 
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