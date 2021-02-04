COMMAND_SYMBOL = "!"

def hasCommandSymbol(content):
    return content[0] == COMMAND_SYMBOL


class Command:
    def __init__(self):
        self.system_methods = {}
    

    # コマンドを追加する
    def addCommand(self, tag, func):
        self.system_methods[tag] = func

    
    # コマンドを実行する
    async def doCommand(self, tag, message):
        await self.system_methods[tag](message)
