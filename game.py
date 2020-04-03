import pygame
import random
import time
import numpy as np  
class Game:

    # defines
    BACK_GROUND_COLOR = 0,0,0
    GREEN = (0, 200, 0 )
    DEFAULT_POS_X = 13

    done = False
    screen = None
    s_w = 0
    s_h = 0
    block = None

    down_rect = None
    up_rect = None
    right_rect = None 

    container = []
    current_arr = []
     
    drop_interval = 1000
    m_time_drop = 0

    score = 0
    next_symbol_arr = []
    current_index = 0
    rand_index = -1  
    t_shape_a = [[ [1, 1, 1],
                   [0, 1, 0],
                 ],
                 [ [0, 1],
                   [1, 1],
                   [0, 1]
                 ],
                 [ [0, 1, 0],
                   [1, 1, 1],
                 ],
                 [ [1, 0],
                   [1, 1],
                   [1, 0]
                 ],
                ]
    
    l_shape_a = [[[ 1, 1],
                  [ 1, 0],
                  [ 1, 0],
                  ],

                 [[ 1, 1, 1],
                  [ 0, 0, 1]],

                 [[ 0, 1],
                  [ 0, 1],
                  [ 1, 1],
                  ],

                 [[ 1, 0, 0],
                  [ 1, 1, 1]],

                ]

    z_shape_a = [[ [ 1, 1, 0],
                   [ 0, 1, 1],
                 ],
                 [ [ 0, 1],
                   [ 1, 1],
                   [ 1, 0],
                 ],
                 [ [ 1, 1, 0],
                   [ 0, 1, 1],
                 ]
               ]
    
    o_shape_a = [[ [ 1, 1],
                   [ 1, 1],
                 ]
                ]

    s_shape_a = [[ [ 0, 1, 1],
                   [ 1, 1, 0],
                 ],
                 [ [ 1, 0],
                   [ 1, 1],
                   [ 0, 1],
                 ]
                ]

    j_shape_a = [[ [ 0, 1],
                   [ 0, 1],
                   [ 1, 1],
                 ],
                 [ [1, 0, 0],
                   [1, 1, 1],
                 ],
                 [ [1, 1],
                   [1, 0],
                   [1, 0]
                 ],
                 [ [1, 1, 1],
                   [0, 0, 1],
                 ],
                ]

    L_shape_a = [[ [ 1],
                   [ 1],
                   [ 1],
                   [ 1],
                 ],
                 [ [1,1,1,1]
                 ]
                ]

    magic_number = 1
    speed_rate = magic_number
    font_size = 25           
    # init method 
    def __init__(self, s_h, s_w):
        self.s_w = s_w
        self.s_h = s_h

        pygame.init()
        self.screen = pygame.display.set_mode((s_w, s_h)) 
        self.screen.fill(self.BACK_GROUND_COLOR)
        self.done = False
        
        self.loadImage()
        self.s_w = 200
        self.s_h = 300

        self.b_width = self.block.get_size()[0]
        self.b_height = self.block.get_size()[1]
        
        self.cols = (self.s_w // self.b_width)-10
        self.rows = self.s_h // self.b_height-10

        self.DEFAULT_POS_X = self.cols//4
        self.DEFAULT_POS_Y = self.rows//4+1

        self.current_x = self.DEFAULT_POS_X
        self.current_y = self.DEFAULT_POS_Y

        self.height = 0
        self.make_2darray()
        self.font = pygame.font.Font(r'./data/HOMOARAK.TTF', self.font_size) 

    # make game array
    def make_2darray(self):
        for j in range(self.rows):
            column = []
            for i in range(self.cols):
                 column.append(0)
            self.container.append(column)

    #gives all possible position 4r current symbol 
    def get_all_move_pos_4r_cur_sym(self):
        a = np.array(self.container)
        a[self.rows-1][1] = 9    
        print (a)
        k = [self.l_shape_a, self.t_shape_a, self.L_shape_a, self.o_shape_a, self.z_shape_a, self.s_shape_a, self.j_shape_a][self.dummy_index]
        for i in range(len(k)):
            s = np.array(k[i])
            print (s)
            row, col = s.shape
            print ('row %d, col %d' %(row,col))
            for r in range(11-col):
                a = np.array(self.container)
                y = 0
                for m in reversed(range(row)):
                    y += 1
                    print ('r=%d' %r)
                    z = r
                    for n in range(col):
                        print (m,n, end=' => ')
                        print (s[m][n])
                        if s[m][n] == 1:
                           if a[self.rows-y][z] == 1:
                              break;
                           else:
                              a[self.rows-y][z] = 1    
                              z += 1 
                        else:
                          z += 1 
                print (a[17:])
            break
    #to display game array        
    def printCurrentArr(self, arr):
        row = len(arr)
        col = len(arr[0])
        for i in range(row):
            for j in range(col):
                print (arr[i][j], end=' ')
            print()

    # draw method to draw the shapes of tetris symbols
    def drawShape(self, arr, x, y):
        row = len(arr)
        col = len(arr[0])
        for i in range(row):
            for j in range(col):
                if arr[i][j] == 1:
                    temp_rect = pygame.Rect(((self.current_x +j)  * self.b_width, (self.current_y+i) * self.b_height, self.b_width, self.b_height)) 
                   # pygame.draw.rect(self.screen, (0,0,255), temp_rect) 
                    if temp_rect.colliderect(self.down_rect):
                        self.dothings(i, j)               
                        return 1
                    self.screen.blit(self.block, ((j + self.current_x) * self.b_width ,  (i+ self.current_y) * self.b_height))

    def drawOnlyShape(self, arr ):
        row = len(arr)
        col = len(arr[0])
        for i in range(row):
            for j in range(col):
                if arr[i][j] == 1:
                    self.screen.blit(self.block, ((j + self.current_x) * self.b_width ,  (i+ self.current_y) * self.b_height))

    # check whether the symbos are touching any other symbols
    def checkcollide(self, rect):
        arr = self.current_arr[self.current_index]
        row = len(arr)
        col = len(arr[0])
        for i in range(row):
           for j in range(col):
               if arr[i][j] == 1: 
                   temp_rect = pygame.Rect(((self.current_x +j)  * self.b_width, (self.current_y+i) * self.b_height, self.b_width, self.b_height)) 
                   #pygame.draw.rect(self.screen, (0,255, 0), temp_rect)
                   if rect.colliderect(self.up_rect):
                       return 2
                   if rect.colliderect(temp_rect): 
                       return 1
        return 0

    # once any symbol is touched, the routine to swap a new symbol and reset positions
    def dothings(self, i, j):
        self.speed_rate = 0
        self.moveUp()
        self.addSymbolToGame(self.current_arr[self.current_index])
        self.current_x = self.DEFAULT_POS_X
        self.current_y = self.DEFAULT_POS_Y
        self.getRandomShape()
        self.speed_rate = self.magic_number
        

    # draw method to draw the shapes of tetris symbols
    def drawContainer(self, arr):
        row = len(arr)
        col = len(arr[0])
        for i in range(row):
            for j in range(col):
                if arr[i][j] == 1:
                    rect = pygame.Rect(( self.b_width *(self.DEFAULT_POS_X+j) , self.b_height *(self.DEFAULT_POS_Y+i), self.b_width, self.b_height))
                    #pygame.draw.rect(self.screen, (255,0, 0), rect)
                    r =  self.checkcollide(rect)
                    if r == 1:
                        self.dothings(i, j)               
                        return 1
                    elif r ==2:
                        self.gameOver() 
                        return 1
                    self.screen.blit(self.block, ( self.b_width *(self.DEFAULT_POS_X+j) , self.b_height *(self.DEFAULT_POS_Y+i)))

    #check if blocks are full
    def checkforfill(self):
        j = 0
        for row in self.container:
            if 0 not in row:
               self.container.remove(row)
               j += 1
               column = []
               for i in range(self.cols):
                   column.append(0)
               self.container.insert(0, column) 
        self.score += j * 10

    # load the basic block of tetris
    def loadImage(self):
        self.block = pygame.image.load(r'./data/roundedBlock.png') 
        self.block = pygame.transform.scale(self.block, (10, 10))
        self.rect = self.block.get_rect()

    # temp method to draw lines
    def drawLine(self, x, y, e_x, e_y):
        pygame.draw.line(self.screen, self.GREEN, [x, y], [e_x, e_y], 1)
        
    # copies the symbol to game array 
    def addSymbolToGame(self, arr):
         row = len(arr)
         col = len(arr[0])
         for i in range(row):
             for j in range(col):
                 if self.container[i+(self.current_y-self.DEFAULT_POS_Y)][j+self.current_x-self.DEFAULT_POS_X] != 1: 
                     self.container[i+(self.current_y-self.DEFAULT_POS_Y)][j+self.current_x-self.DEFAULT_POS_X] = arr[i][j]

    # Generates a new symbol after every touch
    def getRandomShape(self):
        a = [self.l_shape_a, self.t_shape_a, self.L_shape_a, self.o_shape_a, self.z_shape_a, self.s_shape_a, self.j_shape_a]  
        index = random.randint(0,6)
        self.dummy_index = index
        print ('current shape '+ {0:'l_shap', 1:'t_shape', 2:'bar_shape', 3:'o_shape', 4:'z_shaped', 5:'s_shape', 6:'j_shape'}[index])
        self.next_symbol_arr.append(a[index]) 

        if self.rand_index == -1:
            self.current_index = random.randint(0, len(a[index])-1)        
        else:
            self.current_index = self.rand_index 
            self.rand_index = random.randint(0, len(a[index])-1)        

        if len(self.next_symbol_arr)==1:
            index = random.randint(0,6)
            print ('current shape '+ {0:'l_shap', 1:'t_shape', 2:'bar_shape', 3:'o_shape', 4:'z_shaped', 5:'s_shape', 6:'j_shape'}[index])
            self.next_symbol_arr.append(a[index]) 
            self.rand_index = random.randint(0, len(a[index])-1)        

        self.current_arr = self.next_symbol_arr.pop(0) 
        print (self.current_index)

    # Prints the game array
    def printContainer(self):
        for row in self.container:
            print (row)

    # moves the shape one step high
    def moveUp(self):
        self.current_y -= 1
        return 1
         
    # moves the shape one step down
    def moveDown(self):
        self.current_y += 1
        return 1

    # moves the shape one step right
    def moveRight(self):
        if self.current_x < self.rows:
            self.current_x += 1
            return 1
        return 0

    # moves the shape one step left
    def moveLeft(self):
        if self.current_x > self.DEFAULT_POS_X + 0:
            self.current_x -= 1
            return 1
        return 0

    # Handles the game events
    def handleKeyEvent(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.done = True
                return 1
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                   return  self.rotate()
                if event.key == pygame.K_LEFT:
                    return self.moveLeft()
                if event.key == pygame.K_RIGHT:
                   return self.moveRight()
                if event.key == pygame.K_DOWN:
                    self.moveDown()
        return 0

    # Displays GameOver screen
    def gameOver(self):
        self.speed_rate = 0

    # Draws the game rect 
    def drawRectangle(self):
        temp_rect = pygame.Rect((self.DEFAULT_POS_X*self.b_height-2, (self.DEFAULT_POS_Y )  * self.b_height-2   , self.b_width*self.cols+4, self.b_height*self.rows+4)) 
        pygame.draw.rect(self.screen, (255,255, 0), temp_rect, 2)

    # Displays a grid in entire game rect for understanding
    def displayLines(self):
        for i in range(self.rows+1):
                self.drawLine(self.DEFAULT_POS_X*self.b_height, (self.DEFAULT_POS_Y + i)  * self.b_height,  (self.DEFAULT_POS_X * self.b_width)+(self.b_height * self.cols),  (self.DEFAULT_POS_Y + i) * self.b_height)

        for i in range(self.cols+1):
                self.drawLine((self.DEFAULT_POS_X + i )* self.b_height, self.DEFAULT_POS_Y  * self.b_width, (self.DEFAULT_POS_X + i) * self.b_height,(self.DEFAULT_POS_Y  * self.b_width) +(self.b_width * self.rows))

    # to display score, next things
    def drawSecondBox(self):
        pygame.draw.rect(self.screen, (255,255, 0), self.right_rect,2)

    def drawThirdBox(self):
        temp_rect = pygame.Rect(((self.DEFAULT_POS_X+24)*self.b_height, (self.DEFAULT_POS_Y+5)  * self.b_height, self.b_width*7, self.b_height*8))
        pygame.draw.rect(self.screen, (255, 0, 255), temp_rect, 2)  

    def drawFourthBox(self):
        temp_rect = pygame.Rect(((self.DEFAULT_POS_X+24)*self.b_height, (self.DEFAULT_POS_Y+18)  * self.b_height, self.b_width*7, self.b_height*8))
        pygame.draw.rect(self.screen, (255, 0, 255), temp_rect, 2)  

    def drawNextSymbol(self, arr):
        row = len(arr)
        col = len(arr[0])
        for i in range(row):
            for j in range(col):
                if arr[i][j] == 1:
                    self.screen.blit(self.block, ((self.DEFAULT_POS_X+26+j)*self.b_height, (self.DEFAULT_POS_Y+8+i )  * self.b_height))

     # main game loop
    def displayGame(self):
        self.getRandomShape()

        self.down_rect = pygame.Rect((self.DEFAULT_POS_X*self.b_height, (self.DEFAULT_POS_Y + self.rows)  * self.b_height, self.b_width*self.cols, self.b_height)) 
        self.up_rect = pygame.Rect((self.DEFAULT_POS_X*self.b_height, (self.DEFAULT_POS_Y )  * self.b_height, self.b_width*self.cols, self.b_height)) 
        self.right_rect = pygame.Rect(((self.DEFAULT_POS_X+22)*self.b_height, (self.DEFAULT_POS_Y )  * self.b_height-2, self.b_width*12, self.b_height*self.rows+4))
        text_score = self.font.render('SCORE', True, (255, 0, 0)) 
        text_next = self.font.render('NEXT', True, (255, 0, 0)) 
        self.font.set_bold(True)
        text_tetris = self.font.render('TETRIS', True, (0, 0, 255)) 
        while not self.done:
            self.screen.fill(self.BACK_GROUND_COLOR)

            if pygame.time.get_ticks() > self.m_time_drop:
                self.m_time_drop   = pygame.time.get_ticks() + self.drop_interval 
                self.speed_rate += self.speed_rate
           # pygame.draw.rect(self.screen, (255,255, 0), self.down_rect)
            if  self.speed_rate > 1:
                self.current_y += 1
                self.speed_rate = self.magic_number
            
            self.handleKeyEvent()                         
            self.screen.blit(text_tetris, ((self.DEFAULT_POS_X+5)*self.b_height, (2 )  * self.b_height))
            self.displayLines()   
            self.screen.blit(text_next, ((self.DEFAULT_POS_X+23)*self.b_height, (self.DEFAULT_POS_Y+2 )  * self.b_height))
            self.screen.blit(text_score, ((self.DEFAULT_POS_X+22)*self.b_height, (self.DEFAULT_POS_Y+15 )  * self.b_height))
            text_o_score = self.font.render(str(self.score), True, (255, 255, 255)) 
            self.screen.blit(text_o_score, ((self.DEFAULT_POS_X+24)*self.b_height, (self.DEFAULT_POS_Y+21 )  * self.b_height))
            self.drawSecondBox()
            self.drawFourthBox()
            self.drawThirdBox()
            self.drawRectangle()
            self.drawNextSymbol(self.next_symbol_arr[0][self.rand_index])
            self.drawShape(self.current_arr[self.current_index], self.current_x, self.current_y )
            self.drawContainer(self.container)
            self.checkforfill() 
            pygame.display.flip()
 
    # rotates the symbols in the game
    def rotate(self):
        l = len(self.current_arr)
        if l == 1:
          return 0
        self.current_index += 1
        if self.current_index > l-1:
           self.current_index = 0
        return 1

game = Game(400, 400)
game.getRandomShape()
game.get_all_move_pos_4r_cur_sym()
#game.displayGame()
