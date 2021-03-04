from Game.Role.Role import *

class WareWolf(Role):
    def __init__(self):
        super().__init__()

        self.name_tag = RoleNameTag.WAREWOLF
        self.name = GetRoleStringName(self.name_tag)

        self.visible_warewolf_chat = True

        self.victory_condition = VictoryCondition.TYPE_VILLAGER
        self.victory_condition_str = VictoryCondition.ToStr(self.victory_condition)

        self.team = TeamTag.VILLAGER
        self.team_str = TeamTag.ToStr(self.team)


    def GetExplainText(self):
        return self.explain_template.format(self.name, self.team_str, "夜に一人選んで追放できます。", self.victory_condition_str)