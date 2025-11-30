# ship.py
# 飞船类，继承 Sprite，既能单独使用，也能放进 Group()（比如计分板里的小飞船）

import pygame
from pygame.sprite import Sprite


class Ship(Sprite):
    """管理飞船的类"""

    def __init__(self, ai_settings, screen):
        """初始化飞船并设置其初始位置"""
        # 调用父类 Sprite 的初始化，让 Group 知道这是一个精灵
        super().__init__()

        self.screen = screen
        self.ai_settings = ai_settings

        # 加载飞船图像并获取外接矩形
        # 注意路径要和你的项目结构一致：images/ship.bmp
        self.image = pygame.image.load('images/ship.bmp')
        self.rect = self.image.get_rect()
        self.screen_rect = screen.get_rect()

        # 将每艘飞船放在屏幕底部中央
        self.rect.centerx = self.screen_rect.centerx
        self.rect.bottom = self.screen_rect.bottom

        # 保存一个 float 类型的 x 坐标，用于更平滑的移动
        self.center = float(self.rect.centerx)

        # 移动标志（按键控制）
        self.moving_right = False
        self.moving_left = False

    def update(self):
        """根据移动标志调整飞船位置"""
        # 右移
        if self.moving_right and self.rect.right < self.screen_rect.right:
            self.center += self.ai_settings.ship_speed_factor

        # 左移
        if self.moving_left and self.rect.left > 0:
            self.center -= self.ai_settings.ship_speed_factor

        # 根据 self.center 更新 rect.centerx
        self.rect.centerx = self.center

    def blitme(self):
        """在屏幕上绘制飞船"""
        self.screen.blit(self.image, self.rect)

    def center_ship(self):
        """让飞船在屏幕底部居中（例如死亡后重新出现）"""
        self.center = self.screen_rect.centerx
        self.rect.centerx = self.center
        self.rect.bottom = self.screen_rect.bottom
