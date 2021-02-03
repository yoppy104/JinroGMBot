import discord
import json

class Connecter:
    def __init__(self):
        self.JSON_PATH = "Data/connecter.json"

        self.setting = self.readJsonFile()

        self.client = discord.Client()


    def __call__(self):
        self.client.run(self.setting["token"])


    def readJsonFile(self):
        f = open(self.JSON_PATH, "r")
        out = json.load(f)
        f.close()
        return out


    async def Reply(message, content):
        reply = "{} {}".format(message.author.mention, content)
        await message.channel.send(reply)