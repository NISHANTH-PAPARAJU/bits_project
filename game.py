import pygame
import random
import time
import numpy as np  
import datetime
import sys

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

    display = False
    down_rect = None
    up_rect = None
    right_rect = None 

    container = []
    current_arr = []
     
    drop_interval = 1000
    m_time_drop = 0

    use_min_max = False
    score = 0
    next_symbol_arr = []
    current_index = 0
    rand_index = -1  
    t_shape_a = [[ [3, 3, 3],
                   [0, 3, 0],
                 ],
                 [ [0, 3],
                   [3, 3],
                   [0, 3]
                 ],
                 [ [0, 3, 0],
                   [3, 3, 3],
                 ],
                 [ [3, 0],
                   [3, 3],
                   [3, 0]
                 ],
                ]
    
    l_shape_a = [[[ 4, 0],
                  [ 4, 0],
                  [ 4, 4],
                  ],

                 [[ 4, 4, 4],
                  [ 4, 0, 0]],

                 [[ 4, 4],
                  [ 0, 4],
                  [ 0, 4],
                  ],

                 [[ 0, 0, 4],
                  [ 4, 4, 4]],

                ]

    z_shape_a = [[ [ 1, 1, 0],
                   [ 0, 1, 1],
                 ],
                 [ [ 0, 1],
                   [ 1, 1],
                   [ 1, 0],
                 ]]
    
    o_shape_a = [[ [ 2, 2],
                   [ 2, 2],
                 ]
                ]

    s_shape_a = [[ [ 0, 6, 6],
                   [ 6, 6, 0],
                 ],
                 [ [ 6, 0],
                   [ 6, 6],
                   [ 0, 6],
                 ]
                ]

    j_shape_a = [[ [ 0, 5],
                   [ 0, 5],
                   [ 5, 5],
                 ],
                 [ [5, 0, 0],
                   [5, 5, 5],
                 ],
                 [ [5, 5],
                   [5, 0],
                   [5, 0]
                 ],
                 [ [5, 5, 5],
                   [0, 0, 5],
                 ],
                ]

    L_shape_a = [[ [ 7],
                   [ 7],
                   [ 7],
                   [ 7],
                 ],
                 [ [7,7,7,7]
                 ]
                ]

    magic_number = 1
    speed_rate = magic_number
    font_size = 22           
    tittle_font_size = 25
    savepath = r'./save_game/' 
    line=0

    # init method 
    def __init__(self, s_h, s_w, save = False):
        self.s_w = s_w
        self.s_h = s_h

        pygame.init()
        self.screen = pygame.display.set_mode((s_w, s_h)) 
        self.screen.fill(self.BACK_GROUND_COLOR)
        self.done = False
        
        self.loadImage()
        self.s_w = 150
        self.s_h = 350
        
        self.save = save

        if save:
           self.prepareSaveData()

        self.b_width = self.green_block.get_size()[0]
        self.b_height = self.green_block.get_size()[1]
        
        self.cols = 10 
        self.rows = 20

        self.DEFAULT_POS_X = 1#self.cols//4
        self.DEFAULT_POS_Y = 6#self.rows//4+7

        self.current_x = self.DEFAULT_POS_X
        self.current_y = self.DEFAULT_POS_Y

        self.height = 0
        self.make_2darray()
        self.font = pygame.font.Font(r'./data/hemi_head_bd_it.TTF', self.font_size) 
        self.tittle_font = pygame.font.Font(r'./data/HOMOARAK.TTF', self.tittle_font_size) 
        self.getRandomShape()

    def prepareSaveData(self):
        self.filename = datetime.datetime.now().strftime("%Y-%m-%d-%H-%M-%S")   + '.gamedata'
        self.state_np_array = []
        self.action_np_array = []
       
    #make game array
    def make_2darray(self):
        for j in range(self.rows):
            column = []
            for i in range(self.cols):
                 column.append(0)
            self.container.append(column)

    def get_width(self, a, h):
        x = []
        for i in range(self.rows - h, self.rows, 1):
            x.append(np.max(np.where(a[i] == 1)))
        return max(x) 
             
    def get_height(self, a):
        row, col = a.shape
        v = np.argmax(a>0)
        if v:
            return ( row  -  (v//col))
        return 1

    def trackGameState(self):
        if self.save:
            z = np.zeros((20,20), dtype=np.int)
            a = np.array(self.container)
            h = np.array(self.current_arr[self.current_index])
            z[:h.shape[0], :h.shape[1]] = h
            z[:a.shape[0], 5:5+a.shape[1]] = a
            #print ('x:%d' %self.current_x) 
            #print ('index:%d' %self.current_index)
            #print (z)
            action = (self.current_x) + (10*self.current_index)
            #print ('action: %d' %action)
            z[z>0] = 1
            #print (z)
            self.action_np_array.append(action)
            self.state_np_array.append(z)

    def restartGame(self):
        if self.save:
            self.saveGamestate()

        self.make_2darray()
        self.getRandomShape()
        self.prepareSaveData()
        self.line  = 0
        self.score = 0

    def saveGamestate(self): 
        x = np.array(self.state_np_array)
        y = np.array(self.action_np_array)
        np.savez(self.savepath+ self.filename, x, y)

    def getMaxScore(self, a):
        penality = 0
        h = self.get_height(a)
        w = self.get_width(a, h)
        print ('width %d' %w)
        score = 0
        print (a)
        for i in range(self.rows - h, self.rows, 1):
            for j in range(w):
                if  a[i][j]== 0:
                    a[i][j] = penality
                else:
                    a[i][j] = a[i][j] + (abs(penality)+ 1)
                penality -= 1
        #print(a)
        score = np.sum(a)
        print (score)
        return score

    def useMinMax(self):
        scores = []
        all_pos, data_pos = self.get_all_move_pos_4r_cur_sym()
        i = 0
        for  a in all_pos:
            scores.append(self.getMaxScore(a))
            ro, mov = data_pos[i]
            print ('rotate %d , move %d' %(ro, mov))
            i += 1
        print ('scores %s ' %(str(scores)))
        print ('score %d ' %(max(scores)))
        index = (scores.index(max(scores)))
        rotate, move = data_pos[index]
        print ('rotate %d , move %d' %(rotate, move))
        if not self.display:
            return
        count = 0
        while(self.current_index != rotate):
            print ('self.current_index %d ' %(self.current_index))
            self.rotate()
            count += 1
            if count > 6:
                breakpoint()
        count = 0
        while(self.current_x != move+2):
            self.moveRight()
            count += 1
            if count > 6:
                breakpoint()
            print ('self.move %d ' %(self.current_x))

    #gives all possible position 4r current symbol 
    def get_all_move_pos_4r_cur_sym(self):
        data_pos = []
        all_pos = []
        k = self.current_arr
        #k = self.t_shape_a 
        print ('get pos len %d ' %len(k))
        for i in range(len(k)):
            a = np.array(self.container)
            s = np.array(k[i])
            row, col = s.shape
            a_h = self.get_height(a)
            arr_h = row
            for r in range(11-col):
               a = np.array(self.container)
               v =  self.getValidPosition(s, a_h, r, arr_h-1)   
               self.copyPos(v-1, r, s, a)
               all_pos.append(a)
               data_pos.append((i,r))
        return all_pos, data_pos

    def copyPos(self, x, y, arr, a):
        row = len(arr)
        col = len(arr[0])
        for i in reversed(range(row)):
            for j in range(col):
                if arr[i][j] > 0:
                    a[i+x][j+y] = arr[i][j]

    #get valid pos to predication best moves 
    def getValidPosition(self, arr, y_start, x_start, arr_h):
       a = np.array(self.container) 
       row, col = arr.shape
       y = (self.rows-row) - y_start
       while y < self.rows:
           for i in reversed(range(row)):
               for j in range(col):
                   if arr[i][j] > 0:
                       #print( 'i ,j, y %d %d %d' %(i,j,y))
                       if i + y > self.rows-1:
                           return (self.rows)-arr_h 
                       if self.isValidPosition(a, i + y, j+x_start):
                           return y
           y += 1
       return (self.rows)-arr_h

    def isValidPosition(self, a, x,y):
        return a[x][y] > 0  

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
                if arr[i][j] > 0:
                    temp_rect = pygame.Rect(((self.current_x +j)  * self.b_width, (self.current_y+i) * self.b_height, self.b_width, self.b_height)) 
                   # pygame.draw.rect(self.screen, (0,0,255), temp_rect) 
                    if temp_rect.colliderect(self.down_rect):
                        self.dothings(i, j)               
                        return 1
                    self.screen.blit(self.image_arr[arr[i][j]-1], ((j + self.current_x) * self.b_width ,  (i+ self.current_y) * self.b_height))

    def drawOnlyShape(self, arr ):
        row = len(arr)
        col = len(arr[0])
        for i in range(row):
            for j in range(col):
                if arr[i][j] > 0:
                    self.screen.blit(self.image_arr[arr[i][j]-1], ((j + self.current_x) * self.b_width ,  (i+ self.current_y) * self.b_height))

    # check whether the symbos are touching any other symbols
    def checkcollide(self, rect):
        arr = self.current_arr[self.current_index]
        row = len(arr)
        col = len(arr[0])
        for i in range(row):
           for j in range(col):
               if arr[i][j] > 0: 
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
        self.trackGameState()
        self.addSymbolToGame(self.current_arr[self.current_index])
        self.current_x = self.DEFAULT_POS_X
        self.current_y = self.DEFAULT_POS_Y
        self.getRandomShape()
        self.speed_rate = self.magic_number
        self.use_min_max = False

    # draw method to draw the shapes of tetris symbols
    def drawContainer(self, arr):
        row = len(arr)
        col = len(arr[0])
        for i in range(row):
            for j in range(col):
                if arr[i][j] > 0:
                    rect = pygame.Rect(( self.b_width *(self.DEFAULT_POS_X+j) , self.b_height *(self.DEFAULT_POS_Y+i), self.b_width, self.b_height))
                    #pygame.draw.rect(self.screen, (255,0, 0), rect)
                    r =  self.checkcollide(rect)
                    if r == 1:
                        self.dothings(i, j)               
                        return 1
                    elif r ==2:
                        self.restartGame()
                        return 1
                    self.screen.blit(self.image_arr[arr[i][j]-1], ( self.b_width *(self.DEFAULT_POS_X+j) , self.b_height *(self.DEFAULT_POS_Y+i)))

    #check if blocks are full
    def checkforfill(self):
        j = 0
        for row in self.container:
            if 0 not in row:
               self.container.remove(row)
               j += 1
               self.line += 1
               column = []
               for i in range(self.cols):
                   column.append(0)
               self.container.insert(0, column) 
        self.score += j * 10

    # load the basic block of tetris
    def loadImage(self):
        self.green_block = pygame.image.load(r'./data/green.png') 
        self.blue_block = pygame.image.load(r'./data/blue.png') 
        self.yellow_block = pygame.image.load(r'./data/yellow.png') 
        self.orange_block = pygame.image.load(r'./data/orange.png') 
        self.red_block = pygame.image.load(r'./data/red.png') 
        self.sky_blue_block = pygame.image.load(r'./data/sky_blue.png') 
        self.violet_block = pygame.image.load(r'./data/violet.png') 

        self.block1 = pygame.image.load(r'./data/roundedBlock.png') 
        self.block1 = pygame.transform.scale(self.block1, (10, 10))

        self.green_block = pygame.transform.scale(self.green_block, (15, 15))
        self.blue_block = pygame.transform.scale(self.blue_block , (15, 15))
        self.yellow_block = pygame.transform.scale(self.yellow_block, (15, 15))
        self.orange_block = pygame.transform.scale(self.orange_block, (15, 15))
        self.red_block = pygame.transform.scale(self.red_block, (15, 15))
        self.sky_blue_block = pygame.transform.scale(self.sky_blue_block, (15, 15))
        self.violet_block = pygame.transform.scale(self.violet_block, (15, 15))
        self.image_arr  = [self.green_block,self.yellow_block,self.violet_block, self.orange_block,self.blue_block,self.red_block,self.sky_blue_block]
        self.empty_block = pygame.image.load(r'./data/empty.png') 
        self.empty_block = pygame.transform.scale(self.empty_block, (15, 15))
        self.rect = self.green_block.get_rect()

    # temp method to draw lines
    def drawLine(self, x, y, e_x, e_y):
        pygame.draw.line(self.screen, self.GREEN, [x, y], [e_x, e_y], 1)
        
    # copies the symbol to game array 
    def addSymbolToGame(self, arr):
         row = len(arr)
         col = len(arr[0])
         for i in range(row):
             for j in range(col):
                 if self.container[i+(self.current_y-self.DEFAULT_POS_Y)][j+self.current_x-self.DEFAULT_POS_X] == 0: 
                     self.container[i+(self.current_y-self.DEFAULT_POS_Y)][j+self.current_x-self.DEFAULT_POS_X] = arr[i][j]

    # Generates a new symbol after every touch
    def getRandomShape(self):
        a = [self.l_shape_a, self.t_shape_a, self.L_shape_a, self.o_shape_a, self.z_shape_a, self.s_shape_a, self.j_shape_a]  
        index = random.randint(0,6)
        #print ('current shape '+ {0:'l_shap', 1:'t_shape', 2:'bar_shape', 3:'o_shape', 4:'z_shaped', 5:'s_shape', 6:'j_shape'}[index])
        self.next_symbol_arr.append(a[index]) 

        if self.rand_index == -1:
            self.current_index = random.randint(0, len(a[index])-1)        
        else:
            self.current_index = self.rand_index 
            self.rand_index = random.randint(0, len(a[index])-1)        

        if len(self.next_symbol_arr)==1:
            index = random.randint(0,6)
            #print ('current shape '+ {0:'l_shap', 1:'t_shape', 2:'bar_shape', 3:'o_shape', 4:'z_shaped', 5:'s_shape', 6:'j_shape'}[index])
            self.next_symbol_arr.append(a[index]) 
            self.rand_index = random.randint(0, len(a[index])-1)        

        self.current_arr = self.next_symbol_arr.pop(0) 
        #print (self.current_index)

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
        w = np.array(self.current_arr[self.current_index]).shape[1]
        if self.current_x + (w-1) < self.cols:
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
                if self.save:
                    self.saveGamestate()
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
        self.restartGame()
        speed_rate = magic_number

    # Draws the game rect 
    def drawRectangle(self):
        temp_rect = pygame.Rect((self.DEFAULT_POS_X*self.b_height-2, (self.DEFAULT_POS_Y )  * self.b_height-2   , self.b_width*self.cols+4, self.b_height*self.rows+4)) 
        pygame.draw.rect(self.screen, (255,255, 0), temp_rect, 2)

    def drawEmptyBlocks(self):
        for i in range(self.rows):
            for j in range(self.cols):
                    self.screen.blit(self.empty_block, ( self.b_width *(self.DEFAULT_POS_X+j) , self.b_height *(self.DEFAULT_POS_Y+i)))

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

    def drawFourthBox(self,b_width=10, b_height=10):
        for i in range(5):
                self.drawLine((self.DEFAULT_POS_X+22)*b_height, (self.DEFAULT_POS_Y+ 4 + i)  * b_height,  (self.DEFAULT_POS_X + 22) * b_height+((b_width)*6),  (self.DEFAULT_POS_Y+ 4 + i) * (b_height))
        for i in range(5):
                self.drawLine((self.DEFAULT_POS_X+i+22)*b_height, (self.DEFAULT_POS_Y+ 3 )  * b_height,  (self.DEFAULT_POS_X + i + 22) * b_height,  (self.DEFAULT_POS_Y + 3 )*(b_height) + (b_height *6) )
        temp_rect = pygame.Rect(((self.DEFAULT_POS_X+22)*b_height, (self.DEFAULT_POS_Y+3)  * b_height, b_width*6, b_height*6))
        pygame.draw.rect(self.screen, (255, 0, 255), temp_rect, 2)  

    def drawNextSymbol(self, arr):
        row = len(arr)
        col = len(arr[0])
        for i in range(row):
            for j in range(col):
                if arr[i][j] > 0:
                    self.screen.blit(self.image_arr[arr[i][j]-1], ((self.DEFAULT_POS_X+16+j)*self.b_height-5, (self.DEFAULT_POS_Y+3+i )  * self.b_height-5))

     # main game loop
    def displayGame(self):
        self.display = True
        self.down_rect = pygame.Rect((self.DEFAULT_POS_X*self.b_height, (self.DEFAULT_POS_Y + self.rows)  * self.b_height, self.b_width*self.cols, self.b_height)) 
        self.up_rect = pygame.Rect((self.DEFAULT_POS_X*self.b_height, (self.DEFAULT_POS_Y )  * self.b_height, self.b_width*self.cols, self.b_height)) 
        self.right_rect = pygame.Rect(((self.DEFAULT_POS_X+22)*self.b_height, (self.DEFAULT_POS_Y )  * self.b_height-2, self.b_width*12, self.b_height*self.rows+4))
        text_score = self.font.render('SCORE', True, (255, 0, 0)) 
        text_next = self.font.render('NEXT', True, (255, 0, 0)) 
        text_line_tittle = self.font.render('LINE', True, (255, 0, 0)) 
        self.tittle_font.set_bold(True)
        text_tetris = self.tittle_font.render('TETRIS', True, (0, 0, 255)) 
        while not self.done:
            self.screen.fill(self.BACK_GROUND_COLOR)

            if pygame.time.get_ticks() > self.m_time_drop:
                self.m_time_drop   = pygame.time.get_ticks() + self.drop_interval 
                self.speed_rate += self.speed_rate
            #pygame.draw.rect(self.screen, (255,255, 0), self.right_rect)
            if  self.speed_rate > 1:
                self.current_y += 1
                self.speed_rate = self.magic_number
            
            if self.use_min_max and self.current_y == self.rows/2:
                self.use_min_max = False
                self.useMinMax() 

            self.handleKeyEvent()                         
            self.screen.blit(text_tetris, ((self.DEFAULT_POS_X+5)*self.b_height, (2 )  * self.b_height))
            #self.displayLines()   
            self.drawEmptyBlocks()
            self.screen.blit(text_next, ((self.DEFAULT_POS_X+13)*self.b_height, (self.DEFAULT_POS_Y )  * self.b_height))
            self.screen.blit(text_score, ((self.DEFAULT_POS_X+12)*self.b_height, (self.DEFAULT_POS_Y+16 )  * self.b_height))
            text_o_score = self.font.render('{:05d}'.format(self.score), True, (255, 255, 255)) 
            self.screen.blit(text_o_score, ((self.DEFAULT_POS_X+12)*self.b_height, (self.DEFAULT_POS_Y+19 )  * self.b_height))
            self.screen.blit(text_line_tittle, ((self.DEFAULT_POS_X+13)*self.b_height, (self.DEFAULT_POS_Y+10 )  * self.b_height))
            text_line = self.font.render('{:05d}'.format(self.line), True, (255, 255, 255)) 
            self.screen.blit(text_line, ((self.DEFAULT_POS_X+12)*self.b_height, (self.DEFAULT_POS_Y+13 )  * self.b_height))
           # self.drawSecondBox()
            self.drawFourthBox()
            #self.drawThirdBox()
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
    
    def enableMinMax(self):
        self.use_min_max = True

game = Game(400, 302, True)
#game.getRandomShape()
#game.useMinMax()
game.displayGame()
