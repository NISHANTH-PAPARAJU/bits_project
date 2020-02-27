import pygame


class Game:

    BACK_GROUND_COLOR = 0,0,0
    GREEN = (0, 200, 0 )

    done = False
    screen = None
    s_w = 0
    s_h = 0
    block = None

    # init method 
    def __init__(self, s_h, s_w):
        self.s_w = s_w-5
        self.s_h = s_h-5

        pygame.init()
        self.screen = pygame.display.set_mode((s_w, s_h)) 
        self.screen.fill(self.BACK_GROUND_COLOR)
        #pygame.display.update()
        self.done = False

    def loadImage(self):
        self.block = pygame.image.load(r'./data/roundedBlock.png') 
        self.block = pygame.transform.scale(self.block, (10, 10))
        self.screen.blit(self.block, (0, 0))
        pygame.display.flip()

    # temp method to draw lines
    def drawLine(self, x, y, e_x, e_y):
       pygame.draw.line(self.screen, self.GREEN, [x, y], [e_x, e_y], 2)  


    def displayGame(self):
        self.loadImage()
        while not self.done:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.done = True


            b_width = self.block.get_size()[0]
            b_height = self.block.get_size()[1]

            no_w = self.s_w / b_width
            no_h = self.s_h / b_height
            
            for i in range(no_h+1):
                self.drawLine( 0, i * b_height, self.s_w ,  i * b_height)

            for i in range(no_w+1):
                self.drawLine(i * b_width, 0,  i * b_height, self.s_h )

            pygame.display.flip()



game = Game(405, 305)
game.displayGame()
