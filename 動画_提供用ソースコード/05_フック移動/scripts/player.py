import pygame
from scripts.settings import *
from enum import Enum


class PlayerState(Enum):
    IDLE = 1
    PULL = 2


class Player:

    def __init__(self, game, pos, size):
        self.game = game
        self.pos = list(pos)
        self.size = list(size)

        # 画像
        self.image = pygame.Surface(self.size)
        self.image.fill(COLORS["red"])
        self.rect = self.image.get_rect(topleft=self.pos)

        # 状態
        self.state = PlayerState.IDLE

        # 移動
        self.velocity = [0, 0]
        self.speed = 5

        # ジャンプ
        self.jump_speed = 10
        self.can_jump = False

        # フック移動
        self.pull_speed = 20

    def move(self):
        # 左移動
        if self.game.INPUTS["a"]:
            self.velocity[0] = -self.speed
        # 右移動
        elif self.game.INPUTS["d"]:
            self.velocity[0] = self.speed
        else:
            self.velocity[0] = 0

    def jump(self):
        if self.game.INPUTS["w"] and self.can_jump:
            self.velocity[1] = -self.jump_speed
            self.can_jump = False

    def collide(self, direction):
        # 横方向あたり判定
        if direction == "horizontal":
            for tile in self.game.tile_map.tile_list:
                if tile.rect.colliderect(self.rect):
                    # 左移動
                    if self.velocity[0] < 0:
                        self.rect.left = tile.rect.right
                    # 右移動
                    if self.velocity[0] > 0:
                        self.rect.right = tile.rect.left
                    self.pos[0] = self.rect.x
                    if self.state == PlayerState.PULL:
                        self.state = PlayerState.IDLE
                        self.game.hook.is_fixed = False
                        self.velocity = [0, 0]
                    break

        # 縦方向あたり判定
        if direction == "vertical":
            for tile in self.game.tile_map.tile_list:
                if tile.rect.colliderect(self.rect):
                    # 上移動
                    if self.velocity[1] < 0:
                        self.rect.top = tile.rect.bottom
                    # 下移動
                    if self.velocity[1] > 0:
                        self.rect.bottom = tile.rect.top
                        self.can_jump = True
                    self.velocity[1] = 0
                    self.pos[1] = self.rect.y
                    if self.state == PlayerState.PULL:
                        self.state = PlayerState.IDLE
                        self.game.hook.is_fixed = False
                        self.velocity = [0, 0]
                    break

    def idle(self):
        # 重力
        self.velocity[1] += GRAVITY

        # ジャンプ
        self.jump()

        # 移動
        self.move()

        # フック発射
        if self.game.INPUTS["left_click"]:
            self.game.hook.fire(self.rect.center)
        else:
            self.game.hook.can_fire = True
            self.game.hook.is_shooting = False
            self.game.hook.is_fixed = False

        # 位置の更新
        self.pos[0] += self.velocity[0]
        self.rect.x = self.pos[0]
        self.collide("horizontal")

        self.pos[1] += self.velocity[1]
        self.rect.y = self.pos[1]
        self.collide("vertical")

    def pull(self):
        # player -> hook ベクトル
        vector = pygame.math.Vector2(
            self.game.hook.rect.centerx - self.rect.centerx,
            self.game.hook.rect.centery - self.rect.centery
        ).normalize()

        self.velocity[0] = vector.x * self.pull_speed
        self.velocity[1] = vector.y * self.pull_speed

        # 位置の更新
        self.pos[0] += self.velocity[0]
        self.rect.x = self.pos[0]
        self.collide("horizontal")

        self.pos[1] += self.velocity[1]
        self.rect.y = self.pos[1]
        self.collide("vertical")

    def render(self, surface):
        surface.blit(self.image, self.pos)

    def update(self):

        # フック移動
        if self.game.hook.is_fixed:
            if self.game.INPUTS["right_click"]:
                self.state = PlayerState.PULL

        # 通常時
        if self.state == PlayerState.IDLE:
            self.idle()
        # フック移動時
        elif self.state == PlayerState.PULL:
            self.pull()

