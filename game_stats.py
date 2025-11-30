# game_stats.py
# 游戏运行期间用于跟踪游戏状态，如生命数、得分等

class GameStats:
    """跟踪游戏统计信息"""
    def __init__(self, ai_settings):
        """初始化统计信息"""
        self.ai_settings = ai_settings
        self.reset_stats()
        self.game_active = False  # 游戏刚启动时处于非活动状态

        # 最高得分：从文件读取，如果没有文件就用 0
        self.high_score = self.load_high_score()

    def reset_stats(self):
        """初始化运行期间可能变化的统计信息"""
        self.ships_left = self.ai_settings.ship_limit
        self.score = 0
        self.level = 1

    # 新增：从文件读取最高分
    def load_high_score(self):
        filename = "high_score.txt"
        try:
            with open(filename, "r", encoding="utf-8") as f:
                contents = f.read().strip()
                return int(contents) if contents else 0
        except (FileNotFoundError, ValueError):
            return 0

    # 新增：把最高分写入文件
    def save_high_score(self):
        filename = "high_score.txt"
        with open(filename, "w", encoding="utf-8") as f:
            f.write(str(self.high_score))
