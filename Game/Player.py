class Player:
    def __init__(self, member, _player_id):
        # ユーザー情報
        self.user = member
        self.mention = member.mention

        # プレイヤー番号
        self.player_id = _player_id

        # 役職
        self.role = None

        # 生存フラグ
        self.is_alive = True
    

    def setRole(self, _role):
        self.role = _role