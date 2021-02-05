from System.Connecter import Connecter
from System.Command import *
from System.Assert import *
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
        await connecter.Reply(message.author.mention, message.channel, permissionError("Admin Only"))
        return
    name = message.content.split(" ")[1]
    new_ch = await connecter.createChannelFromMessage(message, name)
    connecter.addChannelIDs(name, new_ch.id)
    await connecter.Reply(message.author.mention, message.channel, "チャンネル<<{}>>を作成しました。".format(name))
    await connecter.Reply(new_ch.mention, new_ch, "作成しました。")

# コマンドリストの送信
async def SendCommandList(message):
    command_txt = command.getCommands()
    embed = discord.Embed(title="Command List", description="")
    embed.add_field(name="コマンド名", value=command_txt["command"])
    embed.add_field(name="説明", value=command_txt["explain"])
    embed.add_field(name="引数", value=command_txt["args"])
    await message.channel.send(embed=embed)

# テキストchannel内のログを全て削除する。
async def CleanUp(message):
    if not message.author.guild_permissions.administrator:
        await connecter.Reply(message.author.mention, message.channel, permissionError("Admin Only"))
        return
    async def do(payload):
        if payload.emoji.name == EMOJI["ok"]:
            await connecter.CleanUp(message.channel)
            return True
        elif payload.emoji.name == EMOJI["ng"]:
            await connecter.Send(channel, "!cleanupの実行をやめます")
            return True
        return False
        
    command.addStackMethod(message.channel, do)
    await CheckOK(message.author.mention, message.channel, "全てのログを削除します。よろしいですか？")

# 許諾ダイアログを送信する
async def CheckOK(mention, channel, content):
    command.send_emoji.append(EMOJI["ok"])
    command.send_emoji.append(EMOJI["ng"])
    await connecter.Reply(mention, channel, content)


# Commandの登録
command.addCommand("!ping", PingPong, "接続チェック。 なし")
command.addCommand("!command", SendCommandList, "コマンドのリストを返す。 なし")
command.addCommand("!cleanup", CleanUp, "ログを全て削除する。管理者限定。 なし")
command.addCommand("!mkch", MKChannel, "チャンネルを作成する。管理者限定 チャンネル名")


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
        if len(command.send_emoji) != 0:
            for emoji in command.send_emoji:
                await message.add_reaction(emoji)
            command.send_emoji.clear()
        return

    if hasCommandSymbol(message.content):
        tag = message.content.split(" ")[0]
        if not await command.doCommand(tag, message):
            await connecter.Send(message.channel, syntaxError("{} is not exist".format(tag)))
    else:
        await connecter.Send(message.channel, syntaxError("First char is '!'"))


# スタンプを受け取った時の処理
@connecter.client.event
async def on_raw_reaction_add(payload):
    if payload.member.bot:
        return

    channel = connecter.GetChannel(payload.channel_id)

    # スタンプが押されたチャンネルに待機メソッドが登録されていないなら処理を止める
    if (not channel in command.stack_method.keys()) or (command.stack_method[channel] == None):
        return

    # メソッドが正常に終了したら待機状態をやめる。
    if await command.stack_method[channel](payload):
        command.InitStackMethod(channel)



if __name__ == "__main__":
    connecter.client.run(connecter.setting["token"])