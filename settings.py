# settings.py
# 用于存储游戏中所有可调节的配置

class Settings:
    """存储游戏《外星人入侵》的所有设置"""

    def __init__(self):
        """初始化游戏的设置"""

        # 屏幕设置
        self.screen_width = 1200
        self.screen_height = 800
        self.bg_color = (230, 230, 230)  # 背景颜色

        # 飞船设置
        self.ship_speed_factor = 1.5
        self.ship_limit = 3  # 飞船可用数量（生命数）

        # 子弹设置
        self.bullet_speed_factor = 3
        self.bullet_width = 3
        self.bullet_height = 15
        self.bullet_color = (60, 60, 60)
        self.bullets_allowed = 5  # 屏幕上允许存在的最大子弹数

        # 外星人设置
        self.alien_speed_factor = 1
        self.fleet_drop_speed = 10
        # fleet_direction: 1 表示向右移动，-1 表示向左
        self.fleet_direction = 1

        # 速度随游戏进行加快
        self.speedup_scale = 1.2
        # 分数提升倍数
        self.score_scale = 1.5
        # 外星人子弹设置
        self.alien_bullet_speed_factor = 2.0      # 向下飞的速度
        self.alien_bullets_allowed = 5            # 屏幕上最多外星人子弹数
        self.alien_bullet_color = (200, 0, 0)     # 外星人子弹颜色
        self.alien_fire_chance = 0.003            # 每帧发射概率，可调大/调小
        # 护盾设置
        self.shield_width = 80
        self.shield_height = 40
        self.shield_color = (0, 200, 200)
        self.shield_hits = 5     # 被击中 5 次后消失

        self.initialize_dynamic_settings()

    def initialize_dynamic_settings(self):
        """初始化随游戏变化的设置"""
        self.ship_speed_factor = 1.5
        self.bullet_speed_factor = 3
        self.alien_speed_factor = 1

        # 1 表示向右，-1 表示向左
        self.fleet_direction = 1

        # 记分设置
        self.alien_points = 50

    def increase_speed(self):
        """提高速度设置和外星人分数"""
        self.ship_speed_factor *= self.speedup_scale
        self.bullet_speed_factor *= self.speedup_scale
        self.alien_speed_factor *= self.speedup_scale

        self.alien_points = int(self.alien_points * self.score_scale)
