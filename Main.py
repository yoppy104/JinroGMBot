from System.Connecter import Connecter
import discord

connecter = Connecter()

# 接続時に起動
@connecter.client.event
async def on_ready():
    print("log in")


# メッセージ受信時に実行
@connecter.client.event
async def on_message(message):
    if message.author.bot:
        return

    if message.content == "/neko":
        await Connecter.Reply(message, 'nya-nn')
    else:
        await message.channel.send(message.content)


if __name__ == "__main__":
    connecter.client.run(connecter.setting["token"])