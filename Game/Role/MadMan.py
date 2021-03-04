from Game.Role.Role import *

class MadMan(Role):
    def __init__(self):
        super().__init__()

        self.name_tag = roleNameTag.MAD_MAN
        self.name = GetRoleStringName(self.name_tag)