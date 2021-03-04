from Game.Role.RoleName import *

# 役職クラスを読み込み
from Game.Role.Village import *
from Game.Role.WareWolf import *
from Game.Role.FortuneTeller import *
from Game.Role.Medium import *
from Game.Role.Knight import *
from Game.Role.MadMan import *


class Role:
    def __init__(self):
        pass

    @classmethod
    def GetRoleInstance(cls, name_tag):
        if name_tag == RoleNameTag.VILLAGE
            return Village()
        elif name_tag == RoleNameTag.WAREWOLF:
            return WareWolf()
        elif name_tag == RoleNameTag.FORTUNE_TELLER:
            return FortuneTeller()
        elif name_tag == RoleNameTag.MEDIUM:
            return Medium()
        elif name_tag == RoleNameTag.KNIGHT:
            return Knight()
        elif name_tag == RoleNameTag.MAD_MAN:
            return MadMan()
        