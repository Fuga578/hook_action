import pygame
import sys

from scripts.settings import *
from scripts.tile_map import TileMap
from scripts.player import Player


class Game:

    def __init__(self):
        pygame.init()

        # ウィンドウの設定
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("pygame-hook")

        # FPSの設定
        self.clock = pygame.time.Clock()

        # 入力
        self.INPUTS = {
            "w": False,
            "a": False,
            "s": False,
            "d": False,
            "left_click": False,
            "right_click": False,
        }

        # タイルマップ
        self.tile_map = TileMap(self, tile_size=TILE_SIZE)
        self.tile_map.load()

        # プレイヤー
        self.player = Player(self, pos=(100, 200), size=(20, 20))

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
                if event.key == pygame.K_w:
                    self.INPUTS["w"] = True
                if event.key == pygame.K_a:
                    self.INPUTS["a"] = True
                if event.key == pygame.K_s:
                    self.INPUTS["s"] = True
                if event.key == pygame.K_d:
                    self.INPUTS["d"] = True
            # キーボード開放
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_w:
                    self.INPUTS["w"] = False
                if event.key == pygame.K_a:
                    self.INPUTS["a"] = False
                if event.key == pygame.K_s:
                    self.INPUTS["s"] = False
                if event.key == pygame.K_d:
                    self.INPUTS["d"] = False
            # マウスクリック
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    self.INPUTS["left_click"] = True
                if event.button == 3:
                    self.INPUTS["right_click"] = True
            # マウス開放
            if event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:
                    self.INPUTS["left_click"] = False
                if event.button == 3:
                    self.INPUTS["right_click"] = False

    def run(self):
        while True:

            # 背景の塗りつぶし
            self.screen.fill(COLORS["black"])

            # タイルマップ
            self.tile_map.render(self.screen)

            # プレイヤー
            self.player.update()
            self.player.render(self.screen)

            # イベントの取得
            self.get_events()

            # 更新
            self.clock.tick(FPS)
            pygame.display.update()


if __name__ == "__main__":
    game = Game()
    game.run()
