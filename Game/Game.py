class Game:
    def __init__(self):
        # プレイヤー一覧(alive：生存、dead:死亡)
        self.players = []
        self.alive = []
        self.dead = []

        # 現在の日数
        self.now_day = 0

        # 役職表
        self.role_table = {}

