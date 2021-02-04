from System.Connecter import Connecter
from System.Command import *
import discord

connecter = Connecter()
command = Command()


async def PingPong(message):
    await connecter.Reply(message, "pong")

command.addCommand("!ping", PingPong)

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