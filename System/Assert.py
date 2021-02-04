
class ErrorLog:
    def __init__(self):
        pass

    async def syntaxError(self, channel, message):
        await channel.send("[Syntax Error] {}".format(message))

    
    async def permissionError(self, channel, message):
        await channel.send("[Permission Error] {}".format(message))

    
    async def 