import pygame
import os


def load_image(path, transparent_color=(0, 0, 0), img_size=None):
    img = pygame.image.load(path).convert()
    img.set_colorkey(transparent_color)
    if img_size is not None:
        img = pygame.transform.scale(img, img_size)
    return img


def load_images(path, img_size=None):
    images = []
    for img_name in sorted(os.listdir(path)):
        images.append(load_image(path + '/' + img_name, img_size=img_size))
    return images
