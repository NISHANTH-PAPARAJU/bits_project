import pygame
import random
import time
class Game:

    BACK_GROUND_COLOR = 0,0,0
    GREEN = (0, 200, 0 )
    DEFAULT_POS = 13

    done = False
    screen = None
    s_w = 0
    s_h = 0
    block = None
    
    t_shape = None
    l_shape = None
    z_shape = None
    o_shape = None
    s_shape = None
    j_shape = None
    L_shape = None
  
    container = []
    current_arr = []
    
    current_index = 0
    
    clock = pygame.time.Clock()
    down_rect = None
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
    
    current_x = DEFAULT_POS
    current_y = 0
           
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
        self.s_h = 250


        self.b_width = self.block.get_size()[0]
        self.b_height = self.block.get_size()[1]
        
        self.cols = self.s_w // self.b_width
        self.rows = self.s_h // self.b_height
        print(self.cols)
        self.DEFAULT_POS = self.cols//2
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
                    print ( 'i ,j ' + str(i) +',' + str(j))
                    #self.screen.blit(self.block, ((j + self.current_x) * self.b_width ,  (i+ self.current_y) * self.b_height))
                    temp_rect = pygame.Rect(((self.current_x +j)  * self.b_width, (self.current_y+i) * self.b_height, self.b_width, self.b_height)) 
                    pygame.draw.rect(self.screen, (0,0,255), temp_rect) 
                    if temp_rect.colliderect(self.temp_rect):
                        self.dothings()               

    def checkcollide(self, rect):
        arr = self.current_arr[self.current_index]
        row = len(arr)
        col = len(arr[0])
        for i in range(row):
           for j in range(col):
               if arr[i][j] == 1: 
                   temp_rect = pygame.Rect(((self.current_x +j)  * self.b_width, (self.current_y+i) * self.b_height, self.b_width, self.b_height)) 
                   pygame.draw.rect(self.screen, (0,255, 0), temp_rect)
                   if rect.colliderect(temp_rect): 
                       return True
        return False

    def dothings(self):
        self.speed_rate = 0
        #breakpoint()
        self.printContainer()
        self.addSymbolToGame(self.current_arr[self.current_index])
        self.printContainer()
        self.current_x = self.DEFAULT_POS
        self.current_y = 0
        self.getRandomShape()
        self.speed_rate = self.magic_number
        

    # draw method to draw the shapes of tetris symbols
    def drawContainer(self, arr):
        row = len(arr)
        col = len(arr[0])
        for i in range(row):
            for j in range(col):
                if arr[i][j] == 1:
                    self.screen.blit(self.block, ( self.b_width *j , self.b_height *i))
                    print ('self.anytime ' + str(i) + ',' + str(j))
                    print ('self.current_y ' + str(self.current_y))
                    print ('height '+ str(len(self.current_arr[self.current_index])))
                    print ( (self.current_y + (len(self.current_arr[self.current_index]) + 1)))
                    rect = pygame.Rect(( self.b_width *j , self.b_height *i, self.b_width, self.b_height))
                    pygame.draw.rect(self.screen, (255,0, 0), rect)
                    if self.checkcollide(rect):
                        self.dothings()               
       
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
        #self.screen.blit(self.block, (0, 0))
        #pygame.display.flip()

    # temp method to draw lines
    def drawLine(self, x, y, e_x, e_y):
        pygame.draw.line(self.screen, self.GREEN, [x, y], [e_x, e_y], 2)
        
    def addSymbolToGame(self, arr):
         self.printCurrentArr(arr)
         row = len(arr)
         col = len(arr[0])
         print ( 'c row ' + str(len(self.container)))
         print ( 'c col ' + str(len(self.container[0])))
         for i in range(row):
             for j in range(col):
                 print ('y pos ' + str(j)+ ',' + str(self.current_y-1))
                 print ('x pos ' + str(i+self.current_x))
                 if self.container[i+self.current_y-1][j+self.current_x] != 1: 
                     self.container[i+self.current_y-1][j+self.current_x] = arr[i][j]
         self.printContainer()

    def getRandomShape(self):
        a = [self.l_shape_a, self.t_shape_a, self.L_shape_a, self.o_shape_a, self.z_shape_a, self.s_shape_a, self.j_shape_a]  
        index = 3#random.randint(0,6)
        print ('current shape '+ {0:'l_shap', 1:'t_shape', 2:'bar_shape', 3:'o_shape', 4:'z_shaped', 5:'s_shape', 6:'j_shape'}[index])
        self.current_arr = a[index]
        self.current_index = random.randint(0, len(self.current_arr)-1)        
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

    # main game loop
    def displayGame(self):
        self.getRandomShape()
        self.temp_rect = pygame.Rect((0, (self.rows) * self.b_height, self.b_width*self.rows, self.b_height)) 
      
        while not self.done:
            self.screen.fill(self.BACK_GROUND_COLOR)
            self.speed_rate += self.speed_rate
            pygame.draw.rect(self.screen, (255,255, 0), self.temp_rect)
            if  self.speed_rate > 1:
                self.current_y += 1
                self.speed_rate = self.magic_number
            
            self.handleKeyEvent()                         
            for i in range(self.rows+1):
                self.drawLine( 0, i * self.b_height, self.s_w ,  i * self.b_height)

            for i in range(self.cols+1):
                self.drawLine(i * self.b_width, 0,  i * self.b_height, self.s_h )
                
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

game = Game(400, 300)
game.displayGame()
