import pygame
from .base import Base

class Player(Base):
    width = height = 50

    def __init__(self, startx, starty, image):
        super().__init__(0, 0, image)
        self.size = 32 # TODO PARAMETERS
        self.velocity = 2 # TODO PARAMETERS
        self.image = image
        self.rect = pygame.Rect(startx, starty, self.size, self.size)

    def draw(self, g):
        g.blit(self.image, self.rect)
    
    def handle_collisions(self, other):
        # TODO Improve side detection
        if self.rect.colliderect(other.rect):
            if self.rect.top > other.rect.top:
                self.rect.y += 5
            elif self.rect.left > other.rect.left:
                self.rect.x += 5
            elif self.rect.right < other.rect.right:
                self.rect.x -= 5
            elif self.rect.bottom < other.rect.bottom:
                self.rect.y -= 5

    def handle_keys(self, width, height):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_RIGHT] and self.rect.right < width - self.size : self.rect.x += self.velocity

        if keys[pygame.K_LEFT] and self.rect.left > 0: self.rect.x -= self.velocity

        if keys[pygame.K_UP] and self.rect.top > 0: self.rect.y -= self.velocity

        if keys[pygame.K_DOWN] and self.rect.bottom < height - self.size: self.rect.y += self.velocity