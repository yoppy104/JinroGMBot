from Game.Role.Role import *
from Game.Role.RoleName import *

class FortuneTeller(Role):
    def __init__(self):
        super().__init__()

        self.name_tag = RoleNameTag.FORTUNE_TELLER
        self.name = GetRoleStringName(self.name_tag)

        self.victory_condition = VictoryCondition.TYPE_VILLAGER
        self.victory_condition_str = VictoryCondition.ToStr(self.victory_condition)

        self.team = TeamTag.VILLAGER
        self.team_str = TeamTag.ToStr(self.team)


    def GetExplainText(self):
        return self.explain_template.format(self.name, self.team_str, "夜に一人選んで人狼かどうか知ることができます。", self.victory_condition_str)