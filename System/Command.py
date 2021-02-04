COMMAND_SYMBOL = "!"

def hasCommandSymbol(content):
    return content[0] == COMMAND_SYMBOL


class Command:
    def __init__(self):
        self.system_methods = {}
        self.command_list = {}
    

    # コマンドを追加する
    def addCommand(self, tag, func, explain=""):
        assert tag[0] == "!"
        self.system_methods[tag] = func
        self.command_list[tag] = explain


    def __str__(self):
        txt = ""
        for key in self.command_list.keys():
            txt += "{} : {}\n".format(key, self.command_list[key])
        return txt

    
    # コマンドを実行する
    async def doCommand(self, tag, message):
        if not tag in self.system_methods.keys():
            return False
        await self.system_methods[tag](message)
        return True
