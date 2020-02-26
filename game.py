import pygame


class Game:

    BACK_GROUND_COLOR = 0,0,0

    done = False
    screen = None

    # init method 
    def __init__(self, S_H, S_W):
        pygame.init()
        self.screen = pygame.display.set_mode( (S_W, S_H)) 
        self.screen.fill(self.BACK_GROUND_COLOR)
        #pygame.display.update()
        self.done = False

    def loadImage(self):
        image = pygame.image.load(r'./data/roundedBlock.png') 
        self.screen.blit(image, (0, 0))

    def displayGame(self):
        while not self.done:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.done = True

            self.loadImage()
            #self.screen.fill(self.BACK_GROUND_COLOR)
            pygame.display.flip()


game = Game(400, 300)
game.displayGame()
