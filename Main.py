from System.Connecter import Connecter
from System.Command import *
import discord

connecter = Connecter()
command = Command()


# Command用メソッド
async def PingPong(message):
    await connecter.Reply(message, "pong")

async def MKChannel(message):
    name = message.content.split(" ")[1]
    new_ch = await connecter.createChannelFromMessage(message, name)
    connecter.addChannelIDs(name, new_ch.id)
    await connecter.Reply(message, "チャンネル<<{}>>を作成しました。".format(name))
    await connecter.Reply(new_ch.mention, new_ch, "作成しました。")

# Commandの登録
command.addCommand("!ping", PingPong)
command.addCommand("!mkch", MKChannel)


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
        await command.doCommand(tag, message)



if __name__ == "__main__":
    connecter.client.run(connecter.setting["token"])