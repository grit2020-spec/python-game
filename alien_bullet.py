# alien_bullet.py
import pygame
from pygame.sprite import Sprite

class AlienBullet(Sprite):
    """外星人向下发射的子弹"""

    def __init__(self, ai_settings, screen, alien):
        super().__init__()
        self.screen = screen

        # 子弹大小复用玩家子弹设置
        self.rect = pygame.Rect(
            0, 0,
            ai_settings.bullet_width,
            ai_settings.bullet_height
        )
        # 从外星人底部中心发射
        self.rect.centerx = alien.rect.centerx
        self.rect.top = alien.rect.bottom

        self.y = float(self.rect.y)

        self.color = ai_settings.alien_bullet_color
        self.speed_factor = ai_settings.alien_bullet_speed_factor

    def update(self):
        """子弹向下移动"""
        self.y += self.speed_factor
        self.rect.y = self.y

    def draw_bullet(self):
        pygame.draw.rect(self.screen, self.color, self.rect)
