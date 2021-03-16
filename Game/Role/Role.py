from Game.Role.RoleName import *
from enum import Enum

# 陣営
class TeamTag(Enum):
    VILLAGER = 0,
    WAREWOLF = 1

    @classmethod
    def ToStr(cls, team):
        if team == TeamTag.VILLAGER:
            return "村人陣営"
        elif team == TeamTag.WAREWOLF:
            return "人狼陣営"


class VictoryCondition(Enum):
    TYPE_VILLAGER = 0,
    TYPE_WAREWOLF = 1

    @classmethod
    def ToStr(cls, condition):
        if condition == VictoryCondition.TYPE_VILLAGER:
            return "人狼を全員追放する"
        elif condition == VictoryCondition.TYPE_WAREWOLF:
            return "村人陣営の人数が人狼の数以下になる"



class Role:
    def __init__(self):
        self.name_tag = None
        self.name = None
        self.team = None
        self.victory_condition = None

        self.visible_warewolf_chat = False

        self.explain_template = "あなたの役職は「{}」です。\n　陣営　 : {}\n　能力　 : {}\n勝利条件 : {}"

    # 役職クラスのインスタンスを取得
    @classmethod
    def GetRoleInstance(cls, name_tag):
        # 村人
        if name_tag == RoleNameTag.VILLAGER:
            from Game.Role.Villager import Villager
            return Villager()

        # 人狼
        elif name_tag == RoleNameTag.WAREWOLF:
            from Game.Role.WareWolf import WareWolf
            return WareWolf()

        # 占い師
        elif name_tag == RoleNameTag.FORTUNE_TELLER:
            from Game.Role.FortuneTeller import FortuneTeller
            return FortuneTeller()

        # 霊媒師
        elif name_tag == RoleNameTag.MEDIUM:
            from Game.Role.Medium import Medium
            return Medium()

        # 騎士
        elif name_tag == RoleNameTag.KNIGHT:
            from Game.Role.Knight import Knight
            return Knight()
        
        # 狂人
        elif name_tag == RoleNameTag.MAD_MAN:
            from Game.Role.MadMan import MadMan
            return MadMan()


    def GetExplainText(self):
        return self.explain_template.format(self.name, self.team, "役職が割り当てられていません")

    
    def onNight(self, game):
        pass

    def onFirstNight(self, game):
        pass

    def onMorning(self, game):
        pass

    def onDead(self, game):
        pass

    def onCO(self, game):
        pass
        