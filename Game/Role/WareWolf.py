from Game.Role.Role import *

class WareWolf(Role):
    def __init__(self):
        super().__init__()

        self.name_tag = roleNameTag.WAREWOLF
        self.name = GetRoleStringName(self.name_tag)