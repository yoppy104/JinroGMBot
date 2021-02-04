import discord
import json

class Connecter:
    def __init__(self):
        self.JSON_PATH = "Data/connecter.json"
        self.CHANNEL_IDS_PATH = "Data/channel_ids.json"

        self.setting = self.readJsonFile(self.JSON_PATH)
        self.channel_ids = self.readJsonFile(self.CHANNEL_IDS_PATH)

        self.client = discord.Client()


    def __call__(self):
        self.client.run(self.setting["token"])


    def readJsonFile(self, path):
        f = open(path, "r")
        out = json.load(f)
        f.close()
        return out

    def addChannelIDs(self, name, ch_id):
        self.channel_ids[name] = ch_id

    # channelIDを取得する。
    def GetChannel(self, channel_name):
        ch_id = self.channel_ids[channel_name]
        return self.client.get_channel(ch_id)


    # 特定のチャンネルにメッセージを送信する。
    async def Send(self, channel, content):
        await channel.send(content)


    # メンション付きで返信する。
    async def Reply(self, message, content):
        await self.Reply(message.author.mention, message.channel, reply)

    # メンション付きで送信する。
    async def Reply(self, mention, channel, content):
        reply = "{} {}".format(mention, content)
        await self.Send(channel, reply)

    
    # messageからチャンネルの生成を行う
    async def createChannelFromMessage(self, message, channel_name):
        category_id = message.channel.category_id
        category = message.guild.get_channel(category_id)
        return await self.createChannel(category, channel_name)

    # カテゴリにチャンネルを作成する。
    async def createChannel(self, category, channel_name):
        new_channel = await category.create_text_channel(name=channel_name)
        return new_channel

