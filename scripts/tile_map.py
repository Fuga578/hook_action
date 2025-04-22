import pygame
import csv
from scripts.settings import *


class Tile:

    def __init__(self, game, image, pos, tile_size):
        self.game = game
        self.image = image
        self.pos = list(pos)
        self.tile_size = tile_size

        # 画像
        # self.image = pygame.Surface((self.tile_size, self.tile_size))
        # self.image.fill(COLORS["green"])
        self.rect = self.image.get_rect(topleft=self.pos)

    def render(self, surface, offset=(0, 0)):
        surface.blit(self.image, (self.pos[0] - offset[0], self.pos[1] - offset[1]))


class TileMap:

    def __init__(self, game, tile_size):
        self.game = game
        self.tile_size = tile_size

        # タイル一覧
        self.tile_list = []

    def load(self):
        tile_map = []
        with open("assets/map/map.csv", newline='') as csvfile:
            reader = csv.reader(csvfile)
            for row in reader:
                tile_map.append([int(cell) for cell in row])

        for row_index, row in enumerate(tile_map):
            for col_index, col in enumerate(row):
                if col != 0:
                    print(col)
                    image = self.game.assets["tile"][int(col)-1]
                    tile = Tile(self.game, image, (col_index * self.tile_size, row_index * self.tile_size), self.tile_size)
                    self.tile_list.append(tile)

    def render(self, surface, offset=(0, 0)):
        for tile in self.tile_list:
            tile.render(surface, offset)
