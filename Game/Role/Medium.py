from Game.Role.Role import *

class Medium(Role):
    def __init__(self):
        super().__init__()

        self.name_tag = roleNameTag.MEDIUM
        self.name = GetRoleStringName(self.name_tag)