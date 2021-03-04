from Game.Role.Role import *

class Medium(Role):
    def __init__(self):
        super().__init__()

        self.name_tag = RoleNameTag.MEDIUM
        self.name = GetRoleStringName(self.name_tag)

        self.victory_condition = VictoryCondition.TYPE_VILLAGER
        self.victory_condition_str = VictoryCondition.ToStr(self.victory_condition)

        self.team = TeamTag.VILLAGER
        self.team_str = TeamTag.ToStr(self.team)


    def GetExplainText(self):
        return self.explain_template.format(self.name, self.team_str, "夜にその日の昼間に追放された人が人狼だったかわかります。", self.victory_condition_str)