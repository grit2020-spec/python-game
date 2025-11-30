# game_functions.py
# 负责处理所有用户输入、游戏行为、碰撞检测等核心逻辑
from shield import Shield    # 新增
import sys
import pygame
from bullet import Bullet
from alien import Alien
from time import sleep
import random          # 新增
from alien_bullet import AlienBullet   # 新增
# game_functions.py

def check_keydown_events(event, ai_settings, screen, stats, ship, bullets):
    """按键按下事件"""
    if event.key == pygame.K_RIGHT:
        ship.moving_right = True

    elif event.key == pygame.K_LEFT:
        ship.moving_left = True

    elif event.key == pygame.K_SPACE:
        fire_bullet(ai_settings, screen, ship, bullets)

    elif event.key == pygame.K_q:
        # 退出前保存最高分
        stats.save_high_score()
        sys.exit()



def check_keyup_events(event, ship):
    """按键抬起事件"""
    if event.key == pygame.K_RIGHT:
        ship.moving_right = False

    elif event.key == pygame.K_LEFT:
        ship.moving_left = False


# game_functions.py 中的 check_events

def check_events(ai_settings, screen, stats, sb, play_button, ship, aliens, bullets,shields):
    """响应键盘和鼠标事件"""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            # 退出前保存最高分
            stats.save_high_score()
            sys.exit()

        elif event.type == pygame.KEYDOWN:
            check_keydown_events(event, ai_settings, screen, stats, ship, bullets)

        elif event.type == pygame.KEYUP:
            check_keyup_events(event, ship)


        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            check_play_button(ai_settings, screen, stats, sb, play_button,
                              ship, aliens, bullets, shields,
                              mouse_x, mouse_y)

def check_play_button(ai_settings, screen, stats, sb, play_button,
                      ship, aliens, bullets, shields,
                      mouse_x, mouse_y):
    """玩家点击Play按钮开始游戏"""
    # 检查鼠标是否点击在按钮区域
    button_clicked = play_button.rect.collidepoint(mouse_x, mouse_y)

    # 只有在点击到了按钮，并且当前游戏是非活动状态时，才开始新一局
    if button_clicked and not stats.game_active:
        # 1. 恢复动态设置（子弹速度、外星人速度等）
        ai_settings.initialize_dynamic_settings()

        # 2. 隐藏鼠标光标
        pygame.mouse.set_visible(False)

        # 3. 重置统计信息
        stats.reset_stats()
        stats.game_active = True

        # 4. 重新绘制记分牌上的各项数据
        sb.prep_score()
        sb.prep_high_score()
        sb.prep_level()
        sb.prep_ships()

        # 5. 清空外星人、玩家子弹、护盾
        aliens.empty()
        bullets.empty()
        shields.empty()

        # 6. 重新创建外星人舰队、让飞船回到底部中央、重建护盾
        create_fleet(ai_settings, screen, ship, aliens)
        ship.center_ship()
        create_shields(ai_settings, screen, ship, shields)


def update_screen(ai_settings, screen, stats, sb,
                  ship, aliens, bullets, play_button,
                  alien_bullets=None, shields=None):
    """更新屏幕上的图像，并切换到新屏幕"""
    screen.fill(ai_settings.bg_color)

    # 玩家子弹
    for bullet in bullets.sprites():
        bullet.draw_bullet()

    # 外星人子弹
    if alien_bullets:
        for bullet in alien_bullets.sprites():
            bullet.draw_bullet()

    # 护盾（后面 B 部分会用到）
    if shields:
        shields.draw(screen)

    ship.blitme()
    aliens.draw(screen)

    # 显示得分
    sb.show_score()

    # 若游戏处于非活动状态，显示Play按钮
    if not stats.game_active:
        play_button.draw_button()

    pygame.display.flip()
def update_bullets(ai_settings, screen, stats, sb,
                   ship, aliens, bullets, shields=None):
    """更新子弹的位置并删除已消失的子弹"""
    bullets.update()

    # 删除越界子弹
    for bullet in bullets.copy():
        if bullet.rect.bottom <= 0:
            bullets.remove(bullet)

    # 击中外星人
    check_bullet_alien_collisions(ai_settings, screen, stats, sb,
                                  ship, aliens, bullets)

    # 击中护盾
    if shields:
        check_bullet_shield_collisions(bullets, shields)


def check_bullet_alien_collisions(ai_settings, screen, stats, sb,
                                  ship, aliens, bullets):
    """处理子弹与外星人碰撞"""
    collisions = pygame.sprite.groupcollide(bullets, aliens, True, True)

    if collisions:
        for aliens_hit in collisions.values():
            stats.score += ai_settings.alien_points * len(aliens_hit)
        sb.prep_score()
        check_high_score(stats, sb)

    if len(aliens) == 0:
        bullets.empty()
        ai_settings.increase_speed()

        stats.level += 1
        sb.prep_level()

        create_fleet(ai_settings, screen, ship, aliens)


def fire_bullet(ai_settings, screen, ship, bullets):
    """如果子弹未达到限制数量则发射一颗子弹"""
    if len(bullets) < ai_settings.bullets_allowed:
        new_bullet = Bullet(ai_settings, screen, ship)
        bullets.add(new_bullet)


def get_number_aliens_x(ai_settings, alien_width):
    """计算一行可容纳多少个外星人"""
    available_space_x = ai_settings.screen_width - 2 * alien_width
    number_aliens_x = int(available_space_x / (2 * alien_width))
    return number_aliens_x


def get_number_rows(ai_settings, ship_height, alien_height):
    """计算屏幕可以容纳多少行外星人"""
    available_space_y = (ai_settings.screen_height -
                         (3 * alien_height) - ship_height)
    number_rows = int(available_space_y / (2 * alien_height))
    return number_rows


def create_alien(ai_settings, screen, aliens, alien_number, row_number):
    """创建一个外星人并放在当前行"""
    alien = Alien(ai_settings, screen)
    alien_width = alien.rect.width

    alien.x = alien_width + 2 * alien_width * alien_number
    alien.rect.x = alien.x
    alien.rect.y = alien.rect.height + 2 * alien.rect.height * row_number

    aliens.add(alien)

def create_shields(ai_settings, screen, ship, shields):
    """在飞船前面摆几块护盾"""
    shields.empty()
    shield_y = ship.rect.top - 100  # 护盾比飞船高一点

    positions = [
        ai_settings.screen_width * 1 / 4,
        ai_settings.screen_width * 2 / 4,
        ai_settings.screen_width * 3 / 4,
    ]

    for x in positions:
        shield = Shield(ai_settings, screen, x, shield_y)
        shields.add(shield)

def create_fleet(ai_settings, screen, ship, aliens):
    """创建外星人群"""
    alien = Alien(ai_settings, screen)
    number_aliens_x = get_number_aliens_x(ai_settings, alien.rect.width)
    number_rows = get_number_rows(ai_settings, ship.rect.height, alien.rect.height)

    for row_number in range(number_rows):
        for alien_number in range(number_aliens_x):
            create_alien(ai_settings, screen, aliens, alien_number, row_number)


def check_fleet_edges(ai_settings, aliens):
    """外星人到达边缘时整体下移"""
    for alien in aliens.sprites():
        if alien.check_edges():
            change_fleet_direction(ai_settings, aliens)
            break


def change_fleet_direction(ai_settings, aliens):
    """外星人整体下移，并改变方向"""
    for alien in aliens.sprites():
        alien.rect.y += ai_settings.fleet_drop_speed

    ai_settings.fleet_direction *= -1


def ship_hit(ai_settings, screen, stats, sb, ship, aliens, bullets):
    """响应飞船被外星人撞到"""
    if stats.ships_left > 0:
        stats.ships_left -= 1

        sb.prep_ships()

        aliens.empty()
        bullets.empty()

        create_fleet(ai_settings, screen, ship, aliens)
        ship.center_ship()

        sleep(0.5)

    else:
        stats.game_active = False
        pygame.mouse.set_visible(True)


def check_aliens_bottom(ai_settings, screen, stats, sb, ship, aliens, bullets):
    """检查是否有外星人到达屏幕底部"""
    screen_rect = screen.get_rect()
    for alien in aliens.sprites():
        if alien.rect.bottom >= screen_rect.bottom:
            ship_hit(ai_settings, screen, stats, sb, ship, aliens, bullets)
            break
def update_aliens(ai_settings, screen, stats, sb,
                  ship, aliens, bullets, alien_bullets=None):
    """更新外星人群中所有外星人的位置"""
    check_fleet_edges(ai_settings, aliens)
    aliens.update()

    # 随机让外星人发射子弹
    if alien_bullets is not None and random.random() < ai_settings.alien_fire_chance:
        fire_alien_bullet(ai_settings, screen, aliens, alien_bullets)

    # 检测外星人与飞船碰撞
    if pygame.sprite.spritecollideany(ship, aliens):
        ship_hit(ai_settings, screen, stats, sb, ship, aliens, bullets)

    # 检测外星人是否到底
    check_aliens_bottom(ai_settings, screen, stats, sb, ship, aliens, bullets)

def check_bullet_shield_collisions(bullets, shields):
    """处理 子弹 与 护盾 的碰撞"""
    collisions = pygame.sprite.groupcollide(bullets, shields, True, False)
    if collisions:
        for shields_hit in collisions.values():
            for shield in shields_hit:
                shield.hit()

def update(ai_settings, screen, stats, sb, ship, aliens, bullets):
    """统一更新所有元素"""
    update_bullets(ai_settings, screen, stats, sb, ship, aliens, bullets)
    update_aliens(ai_settings, screen, stats, sb, ship, aliens, bullets)
# game_functions.py 末尾增加

def check_high_score(stats, sb):
    """检查是否产生了新的最高分，并更新显示"""
    if stats.score > stats.high_score:
        stats.high_score = stats.score
        sb.prep_high_score()

        # 如果 GameStats 里有保存方法，就顺便存盘
        if hasattr(stats, "save_high_score"):
            stats.save_high_score()
def fire_alien_bullet(ai_settings, screen, aliens, alien_bullets):
    """随机选一个外星人发射子弹"""
    if len(alien_bullets) < ai_settings.alien_bullets_allowed and aliens:
        shooting_alien = random.choice(aliens.sprites())
        new_bullet = AlienBullet(ai_settings, screen, shooting_alien)
        alien_bullets.add(new_bullet)


def update_alien_bullets(ai_settings, screen, stats, sb,
                         ship, aliens, bullets, alien_bullets,
                         shields=None):
    """更新外星人子弹的位置，并检测碰撞"""
    alien_bullets.update()

    # 删除飞出屏幕底部的子弹
    for bullet in alien_bullets.copy():
        if bullet.rect.top >= ai_settings.screen_height:
            alien_bullets.remove(bullet)

    # 与飞船碰撞：扣命
    if pygame.sprite.spritecollideany(ship, alien_bullets):
        alien_bullets.empty()
        ship_hit(ai_settings, screen, stats, sb, ship, aliens, bullets)

    # （如果后面加入护盾，在这里也会处理，先留一个 shields 接口）
    if shields:
        check_bullet_shield_collisions(alien_bullets, shields)
