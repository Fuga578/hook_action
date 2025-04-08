import pygame
from scripts.settings import *


class Hook:

    def __init__(self, game):
        self.game = game

        # 位置
        self.pos = [0, 0]

        # 画像
        self.image = pygame.Surface((10, 10))
        self.image.fill(COLORS["blue"])
        self.rect = self.image.get_rect(topleft=self.pos)

        # 移動
        self.velocity = [0, 0]
        self.speed = 20

        # 発射
        self.can_fire = True
        self.is_shooting = False
        self.is_fixed = False

    def fire(self, fire_pos):
        if self.can_fire:
            self.can_fire = False
            self.is_shooting = True

            self.rect.center = list(fire_pos)
            self.pos[0] = self.rect.x
            self.pos[1] = self.rect.y

            # マウスの位置取得
            mx, my = pygame.mouse.get_pos()

            # player -> mouse ベクトル
            vector = pygame.math.Vector2(
                mx - (self.game.player.rect.centerx - self.game.render_scroll[0]),
                my - (self.game.player.rect.centery - self.game.render_scroll[1])
            ).normalize()
            self.velocity[0] = vector.x * self.speed
            self.velocity[1] = vector.y * self.speed

    def collide(self):
        for tile in self.game.tile_map.tile_list:
            if tile.rect.colliderect(self.rect):
                self.is_shooting = False
                self.is_fixed = True
                break

    def render(self, surface, offset=(0, 0)):
        if self.is_shooting or self.is_fixed:
            surface.blit(self.image, (self.pos[0] - offset[0], self.pos[1] - offset[1]))
            pygame.draw.line(surface,
                             COLORS["white"],
                             (self.game.player.rect.centerx - offset[0], self.game.player.rect.centery - offset[1]),
                             (self.rect.centerx - offset[0], self.rect.centery - offset[1]))

    def update(self):
        if self.is_shooting:
            # 位置の更新
            self.pos[0] += self.velocity[0]
            self.rect.x = self.pos[0]

            self.pos[1] += self.velocity[1]
            self.rect.y = self.pos[1]

            # あたり判定
            self.collide()
