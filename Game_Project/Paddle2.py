import pygame
WHITE = (255,255,255)

class paddle2(pygame.sprite.Sprite):
    def __init__(self, color, width, height):
        super().__init__()

        self.image = pygame.Surface([width, height])
        self.image.fill (WHITE)
        self.image.set_colorkey(WHITE)
#draws a paddle(Rectangle)
        pygame.draw.ellipse(self.image, color, [0,0, width, height])

        self.rect = self.image.get_rect()
#to control paddle:
    def moveLeft2(self, pixels):
        self.rect.x -= pixels
        #To check if youre getting too far off the screen
        if self.rect.x < 0:
            self.rect.x = 0
    def moveRight2(self, pixels):
        self.rect.x += pixels
        #To check if youre getting too far off the screen
        if self.rect.x > 700:
            self.rect.x = 700
                
