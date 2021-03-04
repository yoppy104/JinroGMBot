from Game.Role.Role import *
from Game.Role.RoleName import *

class FortuneTeller(Role):
    def __init__(self):
        super().__init__()

        self.name_tag = roleNameTag.FORTUNE_TELLER
        self.name = GetRoleStringName(self.name_tag)