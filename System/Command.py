COMMAND_SYMBOL = "!"

def hasCommandSymbol(content):
    return content[0] == COMMAND_SYMBOL

def stackMethodDictionary(method, *args):
    return {
        "method": method,
        "args": args
    }


EMOJI = {
    "ok": '✅',
    "ng": '❌'
}

class Command:
    def __init__(self):
        # コマンドから実行されるメソッドの配列
        self.system_methods = {}
        # コマンドの説明をまとめたリスト
        self.command_list = {}
        
        # 送信を待機している絵文字
        self.send_emoji = []

        # 処理を待機しているメソッド
        self.stack_method = {}

    # 待機メソッドを初期化する。
    def InitStackMethod(self, channel):
        if channel == None:
            print("[NULL Reference] InitStackMethod channel is null")
            return
        if not channel in self.stack_method.keys():
            print("[Key Not Found] InitStackMethod channel is not in keys")
            return
        self.stack_method[channel] = None


    # 待機メソッドを追加する。
    def addStackMethod(self, channel, method):
        self.stack_method[channel] = method
    
    

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
    

    def getCommands(self):
        out = {
            "command": "",
            "explain": "",
            "args": ""
        }
        for key in self.command_list.keys():
            temp = self.command_list[key].split(" ")
            out["command"] += "{}\n".format(key)
            out["explain"] += "{}\n".format(temp[0])
            out["args"]    += "{}\n".format(temp[1])
        return out

    
    # コマンドを実行する
    async def doCommand(self, tag, message):
        if not tag in self.system_methods.keys():
            return False
        await self.system_methods[tag](message)
        return True
