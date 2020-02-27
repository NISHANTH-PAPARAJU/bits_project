import pygame


class Game:

    BACK_GROUND_COLOR = 0,0,0
    GREEN = (0, 200, 0 )

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
  
    container = None

    t_shape_a = [ [1, 1, 1],
                  [0, 1, 0]
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
        
        self.cols = self.s_w / self.b_width
        self.rows = self.s_h / self.b_height
        print (self.cols)
        print (self.rows)
        self.container = [[0]*self.cols]*self.rows

    # draw method to draw the shapes of tetris symbols
    def drawShape(self, arr, x, y):
        rows = len(arr)
        cols = len(arr[0])

        x = self.b_height * x
        y = self.b_width * y

        for i in range(cols):
            for j in range(rows):
                try:
                    if arr[j][i] == 1:
                        self.screen.blit(self.block, ((x+ ( self.b_height *i )), (y+ (self.b_width *j))))
                except:
                    print ('error ' + str(i))
                    
    # load the basic block of tetris
    def loadImage(self):
        self.block = pygame.image.load(r'./data/roundedBlock.png') 
        self.block = pygame.transform.scale(self.block, (10, 10))
        #self.screen.blit(self.block, (0, 0))
        #pygame.display.flip()

    # temp method to draw lines
    def drawLine(self, x, y, e_x, e_y):
        pygame.draw.line(self.screen, self.GREEN, [x, y], [e_x, e_y], 2)  

    def addSymbolToGame(self):
        pass
    
    # main game loop
    def displayGame(self):
        #self.drawShape(self.t_shape_a, 0, 0) 
        #self.drawShape(self.l_shape_a, 5, 0) 
        #self.drawShape(self.L_shape_a, 8, 0) 
        self.drawShape(self.container, 0, 0)
        while not self.done:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.done = True

            for i in range(self.rows+1):
                self.drawLine( 0, i * self.b_height, self.s_w ,  i * self.b_height)

            for i in range(self.cols+1):
                self.drawLine(i * self.b_width, 0,  i * self.b_height, self.s_h )

            pygame.display.flip()



game = Game(405, 305)
game.displayGame()
