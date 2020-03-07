import pygame
import random
import time
class Game:

    BACK_GROUND_COLOR = 0,0,0
    GREEN = (0, 200, 0 )
    DEFAULT_POS_X = 13

    done = False
    screen = None
    s_w = 0
    s_h = 0
    block = None
    
    container = []
    current_arr = []
    
    current_index = 0
      
    clock = pygame.time.Clock()
    down_rect = None
    up_rect = None
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

    magic_number = 0.000000000001
    speed_rate = magic_number
               
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
        
        self.cols = self.s_w // self.b_width
        self.rows = self.s_h // self.b_height

        self.DEFAULT_POS_X = self.cols//4
        self.DEFAULT_POS_Y = self.rows//4+1

        self.current_x = self.DEFAULT_POS_X
        self.current_y = self.DEFAULT_POS_Y
        self.make_2darray()
        
    def make_2darray(self):
        for j in range(self.rows):
            column = []
            for i in range(self.cols):
                 column.append(0)
            self.container.append(column)
            
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
                    self.screen.blit(self.block, ((j + self.current_x) * self.b_width ,  (i+ self.current_y) * self.b_height))
                    temp_rect = pygame.Rect(((self.current_x +j)  * self.b_width, (self.current_y+i) * self.b_height, self.b_width, self.b_height)) 
                   # pygame.draw.rect(self.screen, (0,0,255), temp_rect) 
                    if temp_rect.colliderect(self.down_rect):
                        self.dothings()               

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

    def dothings(self):
        self.speed_rate = 0
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
                    self.screen.blit(self.block, ( self.b_width *(self.DEFAULT_POS_X+j) , self.b_height *(self.DEFAULT_POS_Y+i)))
                    rect = pygame.Rect(( self.b_width *(self.DEFAULT_POS_X+j) , self.b_height *(self.DEFAULT_POS_Y+i), self.b_width, self.b_height))
                    #pygame.draw.rect(self.screen, (255,0, 0), rect)
                    r =  self.checkcollide(rect)
                    if r == 1:
                        self.dothings()               
                    elif r ==2:
                        self.gameOver() 

    #check if blocks are full
    def checkforfill(self):
        for row in self.container:
            if 0 not in row:
               self.container.remove(row)
               column = []
               for i in range(self.cols):
                   column.append(0)
               self.container.insert(0, column) 

    # load the basic block of tetris
    def loadImage(self):
        self.block = pygame.image.load(r'./data/roundedBlock.png') 
        self.block = pygame.transform.scale(self.block, (10, 10))
        self.rect = self.block.get_rect()

    # temp method to draw lines
    def drawLine(self, x, y, e_x, e_y):
        pygame.draw.line(self.screen, self.GREEN, [x, y], [e_x, e_y], 1)
        
    def addSymbolToGame(self, arr):
         row = len(arr)
         col = len(arr[0])
         for i in range(row):
             for j in range(col):
                 if self.container[i+(self.current_y-self.DEFAULT_POS_Y)-1][j+self.current_x-self.DEFAULT_POS_X] != 1: 
                     self.container[i+(self.current_y-self.DEFAULT_POS_Y)-1][j+self.current_x-self.DEFAULT_POS_X] = arr[i][j]

    def getRandomShape(self):
        a = [self.l_shape_a, self.t_shape_a, self.L_shape_a, self.o_shape_a, self.z_shape_a, self.s_shape_a, self.j_shape_a]  
        index = 2#random.randint(0,6)
        print ('current shape '+ {0:'l_shap', 1:'t_shape', 2:'bar_shape', 3:'o_shape', 4:'z_shaped', 5:'s_shape', 6:'j_shape'}[index])
        self.current_arr = a[index]
        self.current_index = 0#random.randint(0, len(self.current_arr)-1)        
        print (self.current_index)

    def printContainer(self):
        for row in self.container:
            print (row)

    def handleKeyEvent(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.done = True
                return 1
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    self.rotate()
                    return 1
                if event.key == pygame.K_LEFT:
                    if self.current_x > 0:
                        self.current_x -= 1
                        return 1
                if event.key == pygame.K_RIGHT:
                    if self.current_x < self.rows:
                        self.current_x += 1
                        return 1
                if event.key == pygame.K_DOWN:
                    self.current_y += 1
                    return 1
        return 0
    def gameOver(self):
        self.speed_rate = 0
        breakpoint()  

    def drawRectangle(self):
        temp_rect = pygame.Rect((self.DEFAULT_POS_X*self.b_height-2, (self.DEFAULT_POS_Y )  * self.b_height-2   , self.b_width*self.cols+4, self.b_height*self.rows+4)) 
        pygame.draw.rect(self.screen, (255,255, 0), temp_rect, 2)

    def displayLines(self):
        for i in range(self.rows+1):
                self.drawLine(self.DEFAULT_POS_X*self.b_height, (self.DEFAULT_POS_Y + i)  * self.b_height,  (self.DEFAULT_POS_X * self.b_width)+(self.b_height * self.cols),  (self.DEFAULT_POS_Y + i) * self.b_height)

        for i in range(self.cols+1):
                self.drawLine((self.DEFAULT_POS_X + i )* self.b_height, self.DEFAULT_POS_Y  * self.b_width, (self.DEFAULT_POS_X + i) * self.b_height,(self.DEFAULT_POS_Y  * self.b_width) +(self.b_width * self.rows))
             
    # main game loop
    def displayGame(self):
        self.getRandomShape()
        self.down_rect = pygame.Rect((self.DEFAULT_POS_X*self.b_height, (self.DEFAULT_POS_Y + self.rows)  * self.b_height, self.b_width*self.cols, self.b_height)) 
        self.up_rect = pygame.Rect((self.DEFAULT_POS_X*self.b_height, (self.DEFAULT_POS_Y )  * self.b_height, self.b_width*self.cols, self.b_height)) 

        while not self.done:
            self.screen.fill(self.BACK_GROUND_COLOR)
            self.speed_rate += self.speed_rate
            pygame.draw.rect(self.screen, (255,255, 0), self.up_rect)
            if  self.speed_rate > 1:
                self.current_y += 1
                self.speed_rate = self.magic_number
            
            self.handleKeyEvent()                         
            #self.displayLines()   
            self.drawRectangle()
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
game.displayGame()
