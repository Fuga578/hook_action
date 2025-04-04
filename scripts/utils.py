import pygame


def load_image(path, transparent_color=(0, 0, 0)):
    img = pygame.image.load(path).convert()
    img.set_colorkey(transparent_color)
    return img
