from Game.Role.Role import *

class Villager(Role):
    def __init__(self):
        super().__init__()

        self.name_tag = RoleNameTag.VILLAGER
        self.name = GetRoleStringName(self.name_tag)

        self.victory_condition = VictoryCondition.TYPE_VILLAGER
        self.victory_condition_str = VictoryCondition.ToStr(self.victory_condition)

        self.team = TeamTag.VILLAGER
        self.team_str = TeamTag.ToStr(self.team)


    def GetExplainText(self):
        return self.explain_template.format(self.name, self.team_str, "能力はありません。", self.victory_condition_str)