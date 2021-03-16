from Game.Role.Role import *

class Player:
    def __init__(self, member, _player_id):
        # ユーザー情報
        self.user = member
        if self.user != "GM":
            self.mention = member.mention

        # プレイヤー番号
        self.player_id = _player_id

        # 役職
        self.role_tag = None
        self.role = None

        # 生存フラグ
        self.is_alive = True
    

    # 役職を設定する
    def setRole(self, name_tag):
        self.role_tag = name_tag
        self.role = Role.GetRoleInstance(name_tag)

    
    def onNight(self, game, is_first=False):
        if is_first:
            self.role.onFirstNight(game)
        else:
            self.role.onNight(game)

    def onMorning(self, game):
        self.role.onMorning(game)

    def onDead(self, game):
        self.role.onDead(game)

    def ComingOut(self, game):
        self.role.onCO(game)

