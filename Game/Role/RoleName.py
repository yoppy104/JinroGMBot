import enum

class RoleNameTag(enum.Enum):
    VILLAGE         = 0,            
    WAREWOLF        = 1,
    FORTUNE_TELLER  = 2,
    MEDIUM          = 3,
    KNIGHT          = 4,
    MAD_MAN         = 5


# 役職名を文字列として取得
def GetRoleStringName(name_tag):
    strName = {
        RoleNameTag.VILLAGE:        "村人",
        RoleNameTag.WAREWOLF:       "人狼",
        RoleNameTag.FORTUNE_TELLER: "占い師",
        RoleNameTag.MEDIUM:         "霊媒師",
        RoleNameTag.KNIGHT:         "騎士",
        RoleNameTag.MAD_MAN:        "狂人"
    }

    return strName[name_tag]
        
