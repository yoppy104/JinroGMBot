from Game.Role.Role import *

class MadMan(Role):
    def __init__(self):
        super().__init__()

        self.name_tag = RoleNameTag.MAD_MAN
        self.name = GetRoleStringName(self.name_tag)

        self.victory_condition = VictoryCondition.TYPE_WAREWOLF
        self.victory_condition_str = VictoryCondition.ToStr(self.victory_condition)

        self.team = TeamTag.WAREWOLF
        self.team_str = TeamTag.ToStr(self.team)


    def GetExplainText(self):
        return self.explain_template.format(self.name, self.team_str, "人狼陣営の人間です。占いには人間と出ます。", self.victory_condition_str)