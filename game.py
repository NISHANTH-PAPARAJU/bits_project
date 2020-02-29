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
    
    l_shape_a = [ [ 1, 1],
                  [ 1, 0],
                  [ 1, 0],
                ]

    z_shape_a = [ [ 1, 1, 0],
                  [ 0, 1, 1],
                ]
    
    o_shape_a = [ [ 1, 1],
                  [ 1, 1],
                ]

    s_shape_a = [ [ 0, 1, 1],
                  [ 1, 1, 0],
                ]

    j_shape_a = [ [ 0, 1],
                  [ 0, 1],
                  [ 1, 1],
                ]

    L_shape_a = [  [ 1],
                   [ 1],
                   [ 1],
                   [ 1],
                ]

    magic_number = 0.000000000001
    speed_rate = magic_number
    
    current_x = DEFAULT_POS
    current_y = 0
           
    # init method 
    def __init__(self, s_h, s_w):
        self.s_w = s_w-5
        self.s_h = s_h-5

        pygame.init()
        self.screen = pygame.display.set_mode((s_w, s_h)) 
        self.screen.fill(self.BACK_GROUND_COLOR)
        self.done = False
        
        self.loadImage()

        self.b_width = self.block.get_size()[0]
        self.b_height = self.block.get_size()[1]
        
        self.cols = self.s_w // self.b_width
        self.rows = self.s_h // self.b_height
        self.make_2darray()

    def make_2darray(self):
        for j in range(self.rows):
            column = []
            for i in range(self.cols):
                 column.append(0)
            self.container.append(column)
            

    # draw method to draw the shapes of tetris symbols
    def drawShape(self, arr, x, y):
        x = self.b_height * x
        y = self.b_width * y
        row = len(arr)
        col = len(arr[0])
        for i in range(col):
            for j in range(row):
                if arr[j][i] == 1:
                    self.screen.blit(self.block, ((x+ ( self.b_width  *i )), ((y)+ (self.b_height *j))))
                    if  (((y)+ (self.b_width *j))) > (self.s_h-(self.b_height*2)):
                        self.speed_rate = 0
                        self.addSymbolToGame(self.current_arr[self.current_index])
                        self.current_x = self.DEFAULT_POS
                        self.current_y = 1
                        self.speed_rate = self.magic_number
                    
    # draw method to draw the shapes of tetris symbols
    def drawContainer(self, arr):
        row = len(arr)
        col = len(arr[0])
        for i in range(col):
            for j in range(row):
                
                if arr[j][i] == 1:
                    self.screen.blit(self.block, ( self.b_width *i , self.b_height *j))
                    print ('self.anytime ' + str(j))
                    print ('self.current_y ' + str(self.current_y))
                    print ('height '+ str(len(self.current_arr[self.current_index])))
                    if self.current_y+len(self.current_arr[self.current_index])+1   > j and self.current_x == i:
                        self.speed_rate = 0
                        self.addSymbolToGame(self.current_arr[self.current_index])
                        self.current_x = self.DEFAULT_POS
                        self.current_y = 1
                        self.speed_rate = self.magic_number
                    
                    


                    
    # load the basic block of tetris
    def loadImage(self):
        self.block = pygame.image.load(r'./data/roundedBlock.png') 
        self.block = pygame.transform.scale(self.block, (10, 10))
        #self.screen.blit(self.block, (0, 0))
        #pygame.display.flip()

    # temp method to draw lines
    def drawLine(self, x, y, e_x, e_y):
        pygame.draw.line(self.screen, self.GREEN, [x, y], [e_x, e_y], 2)  

    def addSymbolToGame(self, arr):
         row = len(arr)
         col = len(arr[0])
         for i in range(col):
             for j in range(row):
                 self.container[j+self.current_y][i+self.current_x]= arr[j][i]
                 print ('y pos ' + str(j+self.current_y))

    def getRandomShape(self):
        a = [self.l_shape_a, self.t_shape_a, self.L_shape_a, self.o_shape_a, self.z_shape_a, self.s_shape_a, self.j_shape_a]  
        index = random.randint(0,6)
        self.current_arr = self.t_shape_a#a[index]
    
    # main game loop
    def displayGame(self):
        #self.drawShape(self.t_shape_a, 0, 0) 
        self.getRandomShape()
        
        
        #self.drawShape(self.L_shape_a, 13, 0) 
        #self.drawShape(self.container, 0, 0)
        #self.printContainer()
        #self.drawShape(self.container, 0, 0)
      
        while not self.done:
            self.screen.fill(self.BACK_GROUND_COLOR)
            self.speed_rate += self.speed_rate
            if  self.speed_rate > 1:
                self.current_y += 1
                self.speed_rate = self.magic_number
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.done = True
                if event.type == pygame.KEYDOWN:
                     if event.key == pygame.K_UP:
                         self.rotate()
                     if event.key == pygame.K_LEFT:
                         self.current_x -= 1
                     if event.key == pygame.K_RIGHT:
                         self.current_x += 1
                     if event.key == pygame.K_DOWN:
                         self.current_y += 1
                         
            for i in range(self.rows+1):
                self.drawLine( 0, i * self.b_height, self.s_w ,  i * self.b_height)

            for i in range(self.cols+1):
                self.drawLine(i * self.b_width, 0,  i * self.b_height, self.s_h )
                
            self.drawShape(self.current_arr[self.current_index], self.current_x, self.current_y )
            self.drawContainer(self.container)
            
            pygame.display.flip()

    def rotate(self):
        l = len(self.current_arr)
        self.current_index += 1
        if self.current_index > l-1:
           self.current_index = 0

game = Game(405, 305)
game.displayGame()
