# shield.py
import pygame
from pygame.sprite import Sprite

class Shield(Sprite):
    """飞船前方的护盾，可被子弹逐渐打碎"""

    def __init__(self, ai_settings, screen, x, y):
        super().__init__()
        self.screen = screen
        self.ai_settings = ai_settings

        self.width = ai_settings.shield_width
        self.height = ai_settings.shield_height

        # 用一个纯色矩形表示护盾
        self.image = pygame.Surface((self.width, self.height))
        self.image.fill(ai_settings.shield_color)
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.bottom = y

        # 护盾耐久度
        self.health = ai_settings.shield_hits

    def hit(self):
        """被子弹击中一次"""
        self.health -= 1
        if self.health <= 0:
            self.kill()
        else:
            # 颜色变暗表示受损（简单效果）
            ratio = self.health / self.ai_settings.shield_hits
            shade = int(200 * ratio)
            self.image.fill((0, shade, shade))
