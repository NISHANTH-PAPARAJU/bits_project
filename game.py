import pygame


class Game:
    screen = None
    done = False
    screen = None

    # init method 
    def __init__(self, S_H, S_W):
        pygame.init()
        self.screen = pygame.display.set_mode( (S_W, S_H)) 
        self.done = False

    def loadImage(self):
        image = pygame.image.load(r'.\data\roundedBlock.png') 
        self.screen.blit(image, (0, 0))

    def displayGame(self):
        while not self.done:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.done = True
            self.loadImage()
            pygame.display.flip()


game = Game(400, 300)
game.displayGame()
