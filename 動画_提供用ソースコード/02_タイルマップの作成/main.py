import pygame
import sys

from scripts.settings import *
from scripts.tile_map import TileMap


class Game:

    def __init__(self):
        pygame.init()

        # ウィンドウの設定
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("pygame-hook")

        # FPSの設定
        self.clock = pygame.time.Clock()

        # タイルマップ
        self.tile_map = TileMap(self, tile_size=TILE_SIZE)
        self.tile_map.load()

    def get_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            # キーボード押下
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()

    def run(self):
        while True:

            # 背景の塗りつぶし
            self.screen.fill(COLORS["black"])

            # タイルマップ
            self.tile_map.render(self.screen)

            # イベントの取得
            self.get_events()

            # 更新
            self.clock.tick(FPS)
            pygame.display.update()


if __name__ == "__main__":
    game = Game()
    game.run()
