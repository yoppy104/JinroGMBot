from System.Connecter import Connecter
from System.Command import *
import discord

connecter = Connecter()
command = Command()


# Command用メソッド
# 送受信のチェック
async def PingPong(message):
    await connecter.Reply(message.author.mention, message.channel, "pong")

# テキストchannelの作成
async def MKChannel(message):
    if not message.author.guild_permissions.administrator:
        return
    name = message.content.split(" ")[1]
    new_ch = await connecter.createChannelFromMessage(message, name)
    connecter.addChannelIDs(name, new_ch.id)
    await connecter.Reply(message.author.mention, message.channel, "チャンネル<<{}>>を作成しました。".format(name))
    await connecter.Reply(new_ch.mention, new_ch, "作成しました。")

# コマンドリストの送信
async def SendCommandList(message):
    await connecter.Reply(message.author.mention, message.channel, str(command))

# テキストchannel内のログを全て削除する。
async def CleanUp(message):
    if not message.author.guild_permissions.administrator:
        return
    await connecter.CleanUp(message.channel)

# Commandの登録
command.addCommand("!ping", PingPong, "接続チェック 引数[なし]  備考[]")
command.addCommand("!command", SendCommandList, "コマンドのリストを返す。引数[なし]  備考[]")
command.addCommand("!cleanup", CleanUp, "ログを全て削除する  備考[管理者限定]")
command.addCommand("!mkch", MKChannel, "チャンネルを作成する 　引数[チャンネル名]  備考[管理者限定]")


# 接続時に起動
@connecter.client.event
async def on_ready():
    print("log in")
    general_ch = connecter.GetChannel("general")
    await connecter.Send(general_ch, "Bot Connected.")


# メッセージ受信時に実行
@connecter.client.event
async def on_message(message):
    if message.author.bot:
        return

    if hasCommandSymbol(message.content):
        tag = message.content.split(" ")[0]
        if not await command.doCommand(tag, message):
            await connecter.Send(message.channel, "[Syntax Error] {} is not exist".format(tag))
    else:
        await connecter.Send(message.channel, "[Syntax Error] First char is '!'")



if __name__ == "__main__":
    connecter.client.run(connecter.setting["token"])