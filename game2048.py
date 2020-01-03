# This is the class for display, caculating numbers - tiles - 
# For updating the tiles, there is respawn

class blocks:
    def __init__(self, status): # some basic parameters, status holding the tile values.
        self.status = status
        self.numColor = (230, 230, 200)
        self.nullColor = (70, 230, 240)
        self.side = 120
       
    def disp(self, Canvus): # display the tiles to the screen 
        fontDisp = pygame.font.Font(None, 75)
        for row in range(0, 4):
            for col in range(0, 4):
                if self.status[row, col] == 0:
                    pygame.draw.rect(Canvus, self.nullColor, (5 + row * (self.side + 5), 
                                                              5 + col * (self.side + 5), 
                                                              self.side, self.side))
                else:
                    pygame.draw.rect(Canvus, self.numColor, (5 + row * (self.side + 5), 
                                                              5 + col * (self.side + 5), 
                                                              self.side, self.side))
                    textSurf = fontDisp.render(str(int(self.status[row, col])), True, (0, 0, 0))
                    textSurfRect = textSurf.get_rect()
                    textSurfRect.center = (5 + row * (self.side + 5) + self.side/2, 5 + col * 
                                           (self.side + 5) + self.side/2)
                    Canvus.blit(textSurf, textSurfRect)
        pygame.display.update()
    
    def action(self, userInput): # action is to update the status when up, down, right, left is pressed
        if userInput == pygame.K_RIGHT:
            for col in range(0, 4):
                for row in range(0, 3):
                    if max(self.status[0:4-row, col]) == 0:
                        break
                    while self.status[3-row, col] == 0:
                        self.status[1:4-row, col] = self.status[0:3-row, col]
                        self.status[0, col] = 0
            for col in range(0, 4):    
                for row in range(0, 3):
                    if max(self.status[:, col]) == 0:
                        break
                    if (self.status[3-row, col] != self.status[2-row, col]) or \
                    (self.status[3-row, col] == 0):
                        continue
                    self.status[3-row, col] = 2 * self.status[3-row, col]
                    self.status[1:3-row, col] = self.status[0:2-row, col]
                    self.status[0, col] = 0
            return True
        elif userInput == pygame.K_LEFT:
            for col in range(0, 4):
                for row in range(0, 3):
                    if max(self.status[row:, col]) == 0:
                        break
                    while self.status[row, col] == 0:
                        self.status[row:-1, col] = self.status[row+1:, col]
                        self.status[3, col] = 0
            for col in range(0, 4):    
                for row in range(0, 3):
                    if max(self.status[:, col]) == 0:
                        break
                    if (self.status[row+1, col] != self.status[row, col]) or \
                    (self.status[row, col] == 0):
                        continue
                    self.status[row, col] = 2 * self.status[row, col]
                    self.status[row+1:-1, col] = self.status[row+2:, col]
                    self.status[3, col] = 0
            return True
        elif userInput == pygame.K_DOWN:
            for row in range(0, 4):
                for col in range(0, 3):
                    if max(self.status[row, 0:4-col]) == 0:
                        break
                    while self.status[row, 3-col] == 0:
                        self.status[row, 1:4-col] = self.status[row, 0:3-col]
                        self.status[row, 0] = 0
            for row in range(0, 4):    
                for col in range(0, 3):
                    if max(self.status[row, :]) == 0:
                        break
                    if (self.status[row, 3-col] != self.status[row, 2-col]) or \
                    (self.status[row, 3-col] == 0):
                        continue
                    self.status[row, 3-col] = 2 * self.status[row, 3-col]
                    self.status[row, 1:3-col] = self.status[row, 0:2-col]
                    self.status[row, 0] = 0
            return True
        elif userInput == pygame.K_UP:
            for row in range(0, 4):
                for col in range(0, 3):
                    if max(self.status[row, col:]) == 0:
                        break
                    while self.status[row, col] == 0:
                        self.status[row, col:-1] = self.status[row, col+1:]
                        self.status[row, 3] = 0
            for row in range(0, 4):    
                for col in range(0, 3):
                    if max(self.status[row, :]) == 0:
                        break
                    if (self.status[row, col+1] != self.status[row, col]) or \
                    (self.status[row, col] == 0):
                        continue
                    self.status[row, col] = 2 * self.status[row, col]
                    self.status[row, col+1:-1] = self.status[row, col+2:]
                    self.status[row, 3] = 0
            return True
        elif userInput == pygame.K_r:
            self.status = init_status()
            return True
        else:
            return False
        
    def respawn(self): # generating one extra tile for getting to 2048.
        respX, respY = np.where(self.status == [0])
        respRand = np.random.randint(len(respX))
        self.status[respX[respRand], respY[respRand]] = np.random.randint(1, 2) * 2

def init_status(): # this function to initialize the status 2D array.
    status = np.zeros((4, 4))
    num = 0
    while num < 3:
        inital_row = random.randint(0, 3)
        inital_col = random.randint(0, 3)
        if status[inital_row, inital_col] == 0:
            status[inital_row, inital_col] = random.randint(1, 2) * 2
            num += 1
    return status

import numpy as np
import pygame
import sys
import random

def main():
    pygame.init()
    screen = pygame.display.set_mode([505,505], flags = pygame.RESIZABLE)
    screen.fill((255,255,255))
    pygame.display.update()
    status = init_status()

    gameRun = blocks(status)
    gameRun.disp(screen)
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                statChecker = gameRun.status.copy()
                if gameRun.action(event.key):
                    gameRun.disp(screen)
                    if False in (statChecker == gameRun.status) and event.key!=pygame.K_r:
                        pygame.time.wait(100)
                        gameRun.respawn()
                        gameRun.disp(screen)
                    elif [0] not in np.unique(gameRun.status):
                        print('Game over warning, try all directions. Press R to restart.')
                else:
                    print("Wrong Input! Try again.")

if __name__ == "__main__":
    main()
