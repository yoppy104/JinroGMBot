from Game.Role.RoleName import *

class GameRule:
    def __init__(self):
        # 遺言
        self.is_testament = True

        # 役職の割り当て人数
        self.assign_roles = {
            RoleNameTag.VILLAGER:       0,
            RoleNameTag.WAREWOLF:       1,
            RoleNameTag.FORTUNE_TELLER: 0,
            RoleNameTag.MEDIUM:         0,
            RoleNameTag.KNIGHT:         1,
            RoleNameTag.MAD_MAN:        0
        }

        # 役欠けがありか
        self.is_role_lack = False


    # 役職を割り当てる
    def AssignRole(self, index):
        count_num = 0
        for key in self.assign_roles.keys():
            count_num += self.assign_roles[key]

            if index < count_num:
                return key

        return None

    
    # 役職の割り当て人数を設定する
    def SetNumRole(roleNameTag, num):
        self.assign_roles[roleNameTag] = num