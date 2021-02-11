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
    "ng": '❌',
    "join": '🤚',
    "finish": '🐺'
}

class Command:
    def __init__(self):
        # コマンドから実行されるメソッドの配列
        self.system_methods = {}
        # コマンドの説明をまとめたリスト
        self.command_list = {}
        
        # 送信を待機している絵文字
        self.send_emoji = {}

        # 処理を待機しているメソッド
        self.stack_method = {}

        # 待機処理の実行ダイアログ
        self.check_stack_dialog = {}

    # 待機メソッドを初期化する。
    async def InitStackMethod(self, channel):
        if channel == None:
            print("[NULL Reference] InitStackMethod channel is null")
            return
        if not channel in self.stack_method.keys():
            print("[Key Not Found] InitStackMethod channel is not in keys")
            return
        self.stack_method[channel] = None
        await self.check_stack_dialog[channel].delete()

    
    # 送信する絵文字を追加する。
    def addSendEmoji(self, channel, emoji_list, is_name=False):
        # 名前で送られてきたら絵文字に直す
        if is_name:
            for i in range(len(emoji_list)):
                emoji_list[i] = EMOJI[emoji_list[i]]

        if channel in self.send_emoji.keys():
            self.send_emoji[channel] += emoji_list
        else:
            self.send_emoji[channel] = emoji_list


    # 待機メソッドを追加する。
    def addStackMethod(self, channel, method, message=None):
        self.stack_method[channel] = method
        self.check_stack_dialog[channel] = message
    
    

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
        out = []
        for key in self.command_list.keys():
            temp = self.command_list[key].split(" ")
            out.append(
                {
                    "command": key,
                    "explain": temp[0],
                    "permission": temp[1],
                    "argments": temp[2]
                }
            )
        return out

    
    # コマンドを実行する
    async def doCommand(self, tag, message):
        if not tag in self.system_methods.keys():
            return False
        await self.system_methods[tag](message)
        return True
