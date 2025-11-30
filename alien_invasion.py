# alien_invasion.py
# 整个游戏的启动入口

import pygame
from settings import Settings
from ship import Ship
from game_stats import GameStats
from button import Button
from scoreboard import Scoreboard
import game_functions as gf
from pygame.sprite import Group

def run_game():
    """初始化游戏并创建显示屏幕"""
    pygame.init()
    ai_settings = Settings()
    screen = pygame.display.set_mode(
        (ai_settings.screen_width, ai_settings.screen_height))
    pygame.display.set_caption("Alien Invasion")

    #初始化参数、对象
    play_button = Button(ai_settings, screen, "Play")


    stats = GameStats(ai_settings)
    sb = Scoreboard(ai_settings, screen, stats)

    ship = Ship(ai_settings, screen)
    bullets = Group()
    aliens = Group()
    alien_bullets = Group()
    shields = Group()
    gf.create_fleet(ai_settings, screen, ship, aliens)
    gf.create_shields(ai_settings, screen, ship, shields)
    #事件循环
    while True:
        #业务逻辑的调用
        gf.check_events(ai_settings, screen, stats, sb, play_button,
                        ship, aliens, bullets, shields)

        if stats.game_active:
            ship.update()
            gf.update_bullets(ai_settings, screen, stats, sb,
                              ship, aliens, bullets, shields)
            gf.update_aliens(ai_settings, screen, stats, sb,
                             ship, aliens, bullets, alien_bullets)
            gf.update_alien_bullets(ai_settings, screen, stats, sb,
                                    ship, aliens, bullets, alien_bullets,
                                    shields)

        gf.update_screen(ai_settings, screen, stats, sb,
                         ship, aliens, bullets, play_button,
                         alien_bullets, shields)



run_game()
