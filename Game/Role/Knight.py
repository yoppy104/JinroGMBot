from Game.Role.Role import *

class Knight(Role):
    def __init__(self):
        super().__init__()

        self.name_tag = roleNameTag.KNIGHT
        self.name = GetRoleStringName(self.name_tag)