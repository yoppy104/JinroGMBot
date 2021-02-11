import discord
import json

class Connecter:
    def __init__(self):
        self.JSON_PATH = "Data/connecter.json"
        # self.CHANNEL_IDS_PATH = "Data/channel_ids.json"

        self.setting = self.readJsonFile(self.JSON_PATH)
        # self.channel_ids = self.readJsonFile(self.CHANNEL_IDS_PATH)

        self.client = discord.Client()

    # 初期化
    def Init(self):
        self.guild = discord.utils.get(self.client.guilds, name=self.setting["server_name"])


    def __call__(self):
        self.client.run(self.setting["token"])


    # JSONファイルを読み込む
    def readJsonFile(self, path):
        f = open(path, "r", encoding="UTF-8")
        out = json.load(f)
        f.close()
        return out

    # チャンネルをIDから取得する。
    def GetChannel(self, ch_id):
        return self.guild.get_channel(ch_id)

    # チャンネルを名前から取得する。
    def GetChannelFromName(self, ch_name):
        return discord.utils.get(self.guild.channels, name=ch_name)

    # ユーザーをIDから取得する。
    def GetUser(self, channel, user_id):
        return channel.get_user(user_id)


    # 特定のチャンネルにメッセージを送信する。
    async def Send(self, channel, content):
        if channel == None:
            return
        return await channel.send(content)

    # メンション付きで送信する。
    async def Reply(self, mention, channel, content):
        # メンションの後に改行を入れるかどうか。30文字以上か改行があるなら改行する。
        is_reline = "\n" if (len(content) > 30 or ("\n" in content)) else " "
        reply  = "{}{}{}".format(mention, is_reline, content)
        return await self.Send(channel, reply)

    # カテゴリーをギルド内に作成する
    async def CreateCategory(self, guild, category_name):
        new_category = await guild.create_category(name=category_name)
        return new_category

    # messageからチャンネルの生成を行う
    async def CreateTextChannelFromMessage(self, message, channel_name):
        category_id = message.channel.category_id
        category = message.guild.get_channel(category_id)
        return await self.CreateTextChannel(category, channel_name)

    # カテゴリにチャンネルを作成する。
    async def CreateTextChannel(self, category, channel_name):
        new_channel = await category.create_text_channel(name=channel_name)
        return new_channel

    # ボイスチャンネルを作成する
    async def CreateVoiceChannel(self, category, channel_name):
        new_channel = await category.create_voice_channel(channel_name)
        return new_channel
    
    # テキストチャンネルのログを全消去する。
    async def CleanUp(self, channel):
        await channel.purge()


    # チャンネルの閲覧、送信権限を設定
    async def SetTextChannelPermission(self, channel, target, read=False, send=False, reaction=False, read_history=False):
        await channel.set_permissions(target, read_messages=read, send_messages=send, add_reactions=reaction, read_message_history=read_history)

    
    # チャンネルで強制ミュートを切り替える
    async def SetMute(self, member, is_mute):
        await member.edit(mute=is_mute)