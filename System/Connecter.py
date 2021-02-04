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

    
    def GetChannel(self, channel_name):
        ch_id = self.channel_ids[channel_name]
        return self.client.get_channel(ch_id)


    async def Send(self, channel,content):
        await channel.send(content)


    async def Reply(self, message, content):
        reply = "{} {}".format(message.author.mention, content)
        await self.Send(message.channel, reply)

