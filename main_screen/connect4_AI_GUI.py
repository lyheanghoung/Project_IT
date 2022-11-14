
import numpy as np
import pygame
import sys
import random
import math

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

    SQUARESIZE = 100
    WIDTH = Connect4.NUM_COLS *SQUARESIZE
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
        myfont = pygame.font.SysFont("monospace", 75)
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
                                label = myfont.render("You wins!!!", 1, self.RED)
                            else:
                                label = myfont.render("You wins!!!", 1, self.YELLOW)
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
                                label = myfont.render("You loses!", 1, self.RED)
                            else:
                                label = myfont.render("You loses!", 1, self.YELLOW)
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