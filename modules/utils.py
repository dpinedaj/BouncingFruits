import pygame

def load_image(file_path, width=64, height=64):
    img = pygame.image.load(file_path)
    img = pygame.transform.scale(img, (width, height))

    return img
