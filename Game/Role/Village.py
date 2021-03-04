from Game.Role.Role import *

class Village(Role):
    def __init__(self):
        super().__init__()

        self.name_tag = roleNameTag.VILLAGE
        self.name = GetRoleStringName(self.name_tag)