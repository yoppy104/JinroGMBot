# -*- coding: utf-8 -*-

from System.Connecter import Connecter
from System.Command import *
from System.Assert import *
from Game.Game import *
import discord

connecter = Connecter()
command = Command()
game = Game(connecter, command)
my_assert = ErrorLog()

# Command用メソッド
# 送受信のチェック
async def PingPong(message):
    await connecter.Reply(message.author.mention, message.channel, "pong")

# テキストchannelの作成
async def MKChannel(message):
    if not message.author.guild_permissions.administrator:
        await connecter.Reply(message.author.mention, message.channel, my_assert.permissionError("Admin Only"))
        return
    name = message.content.split(" ")[1]
    new_ch = await connecter.CreateTextChannelFromMessage(message, name)
    connecter.addChannelIDs(name, new_ch.id)
    await connecter.Reply(message.author.mention, message.channel, "チャンネル<<{}>>を作成しました。".format(name))
    await connecter.Reply(new_ch.mention, new_ch, "作成しました。")

# コマンドリストの送信
async def SendCommandList(message):
    command_list = command.getCommands()
    num_command = len(command_list)
    embed_list = []
    for command_value in command_list:
        mini_embed = discord.Embed(title=command_value["command"], description="")
        mini_embed.add_field(name="説明", value=command_value["explain"])
        mini_embed.add_field(name="権限", value=command_value["permission"])
        mini_embed.add_field(name="引数", value=command_value["argments"])
        embed_list.append(mini_embed)
    for embed in embed_list:
        await message.channel.send(embed=embed)

# テキストchannel内のログを全て削除する。
async def CleanUp(message):
    if not message.author.guild_permissions.administrator:
        await connecter.Reply(message.author.mention, message.channel, my_assert.permissionError("Admin Only"))
        return
    async def do(payload):
        if payload.emoji.name == EMOJI["ok"]:
            await command.InitStackMethod(message.channel)
            await connecter.CleanUp(message.channel)
        elif payload.emoji.name == EMOJI["ng"]:
            await command.InitStackMethod(message.channel)
            await connecter.Send(message.channel, "!cleanupの実行をやめます")
    command.addStackMethod(message.channel, do)
    await CheckOK(message.author.mention, message.channel, "全てのログを削除します。よろしいですか？")

# チャンネルの閲覧権限を要求
async def RequirePermission(message):
    arg = message.content.split(" ")
    if len(arg) < 2:
        return
    channel = connecter.GetChannelFromName(arg[1])
    async def do(payload):
        if not payload.member.guild_permissions.administrator:
            return 
        if payload.emoji.name == EMOJI["ok"]:
            await connecter.SetTextChannelPermission(channel, message.author, read=True, send=True, reaction=True, read_history=True)
            await command.InitStackMethod(message.channel)
            await connecter.Send(message.channel, "{} <<{}>>の閲覧権限を付与しました".format(message.author.mention, channel))
            await connecter.Send(channel, "{}が閲覧可能になりました".format(message.author.mention))
        elif payload.emoji.name == EMOJI["ng"]:
            await command.InitStackMethod(message.channel)
            await connecter.Send(message.channel, "{} <<{}>>の権限要求が拒否されました。".format(message.author.mention, channel))

    command.addStackMethod(message.channel, do)
    await CheckOK("管理者様", message.channel, "{}が<<{}>>の閲覧権限を要求しています。".format(message.author.mention, channel))


# 許諾ダイアログを送信する
async def CheckOK(mention, channel, content):
    command.addSendEmoji(channel, ["ok", "ng"], is_name=True)
    message = await connecter.Reply(mention, channel, content)
    command.check_stack_dialog[channel] = message


# 強制ミュート
async def SetMute(message):
    if not message.author.guild_permissions.administrator:
        await connecter.Reply(message.author.mention, message.channel, my_assert.permissionError("Admin Only"))
        return
    ch_name = message.content.split(" ")[1]
    channel = connecter.GetChannelFromName(ch_name)
    if channel == None:        
        await connecter.Reply(message.author.mention, message.channel, my_assert.nullError("{}というボイスチャンネルはありません".format(ch_name)))
        return 
    for member in channel.members:
        if member.bot:
            continue
        await connecter.SetMute(member, True)

# 強制ミュート解除
async def SetDismute(message):
    if not message.author.guild_permissions.administrator:
        await connecter.Reply(message.author.mention, message.channel, my_assert.permissionError("Admin Only"))
        return
    ch_name = message.content.split(" ")[1]
    channel = connecter.GetChannelFromName(ch_name)
    if channel == None:
        await connecter.Reply(message.author.mention, message.channel, my_assert.nullError("{}というボイスチャンネルはありません".format(ch_name)))
        return 
    for member in channel.members:
        if member.bot:
            continue
        await connecter.SetMute(member, False)


# Commandの登録
command.addCommand("!ping", PingPong, "接続チェック everyone なし")
command.addCommand("!command", SendCommandList, "コマンドのリストを返す everyone なし")
command.addCommand("!cleanup", CleanUp, "ログを全て削除する 管理者 なし")
command.addCommand("!mute", SetMute, "チャンネルにいる人を全員、強制ミュートする 管理者 チャンネル名")
command.addCommand("!dismute", SetDismute, "チャンネルにいる人を全員、強制ミュートを解除する 管理者 チャンネル名")
command.addCommand("!mkch", MKChannel, "チャンネルを作成する 管理者 チャンネル名")
command.addCommand("!require_permission", RequirePermission, "テキストチャンネルの閲覧権限を要求する 要管理者許諾 チャンネル名")

# 人狼ゲーム関連のコマンド
command.addCommand("!game_start", game.onStart, "人狼ゲームを開始する everyone なし")


# 接続時に起動
@connecter.client.event
async def on_ready():
    connecter.Init()
    print("log in")
    general_ch = connecter.GetChannelFromName(connecter.setting["general_ch"])
    print(general_ch)
    await connecter.Send(general_ch, "Bot Connected.")


# メッセージ受信時に実行
@connecter.client.event
async def on_message(message):
    # botのメッセージにスタンプを追加する処理
    if message.author.bot:
        if (message.channel in command.send_emoji) and (len(command.send_emoji[message.channel]) != 0):
            for emoji in command.send_emoji[message.channel]:
                await message.add_reaction(emoji)
            command.send_emoji[message.channel].clear()
        return

    # コマンドを実行する処理
    if hasCommandSymbol(message.content):
        tag = message.content.split(" ")[0]
        if not await command.doCommand(tag, message):
            await connecter.Send(message.channel, my_assert.syntaxError("{} is not exist".format(tag)))


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
    await command.stack_method[channel](payload)


if __name__ == "__main__":
    connecter.client.run(connecter.setting["token"])