from Game.Role.Role import *

class Knight(Role):
    def __init__(self):
        super().__init__()

        self.name_tag = RoleNameTag.KNIGHT
        self.name = GetRoleStringName(self.name_tag)

        self.victory_condition = VictoryCondition.TYPE_VILLAGER
        self.victory_condition_str = VictoryCondition.ToStr(self.victory_condition)

        self.team = TeamTag.VILLAGER
        self.team_str = TeamTag.ToStr(self.team)


    def GetExplainText(self):
        return self.explain_template.format(self.name, self.team_str, "夜に一人選んで護衛できます。護衛している人は人狼から襲われません", self.victory_condition_str)