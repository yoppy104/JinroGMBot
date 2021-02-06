class Player:
    def __init__(self):
        # ユーザー情報
        self.user = None
        self.meniton = None

        # プレイヤー番号
        self.player_id = 0

        # 役職
        self.role = None

        # 生存フラグ
        self.is_alive = True
    
    def setRole(self, _role):
        self.role = _role