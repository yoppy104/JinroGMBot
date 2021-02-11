BASIC_CREATE_TEXT_CHANNELS_NAME = [
    "人狼の会合",
    "霊界",
    "掲示板"
]

BASIC_CREATE_VOICE_CHANNELS_NAME = [
    "討論場"
]

from System.Command import EMOJI

class Game:
    def __init__(self, _connecter, _command):
        # プレイヤー一覧(alive：生存、dead:死亡)
        self.players = []
        self.alive = []
        self.dead = []

        # 現在の日数
        self.now_day = 0

        # 役職表
        self.role_table = {}

        self.connecter = _connecter
        self.command = _command

        self.use_category = None
        self.channels = {}

    
    # チャンネル名のリストからテキストチャンネルを取得する。
    async def GetTextChannels(self, channel_list):
        for text_ch in channel_list:
            new_ch = self.connecter.GetChannelFromName(text_ch)
            if new_ch == None:
                new_ch = await self.connecter.CreateTextChannel(self.use_category, text_ch)
            self.channels[text_ch] = new_ch
    
    # チャンネル名のリストからボイスチャンネルを取得する。
    async def GetVoiceChannels(self, channel_list):
        for voice_ch in channel_list:
            new_ch = self.connecter.GetChannelFromName(voice_ch)
            if new_ch == None:
                new_ch = await self.connecter.CreateVoiceChannel(self.use_category, voice_ch)
            self.channels[voice_ch] = new_ch

    # カテゴリを取得する
    async def GetCategory(self, category_name):
        temp = self.connecter.GetCategoryFromName(category_name)
        if temp == None:
            temp = await self.connecter.CreateCategory(self.connecter.guild, category_name)
        return temp
    
    # ゲーム開始によって呼び出される処理
    async def onStart(self, message):
        # ゲームで使用するカテゴリの作成
        self.use_category = await self.GetCategory("人狼ゲーム")
        print(self.use_category)

        # 基本的に使用するチャンネルを取得
        await self.GetTextChannels(BASIC_CREATE_TEXT_CHANNELS_NAME)
        await self.GetVoiceChannels(BASIC_CREATE_VOICE_CHANNELS_NAME)

        await self.connecter.Reply(message.author.mention, message.channel, "{}で参加者を募ります".format("掲示板"))

        for value in self.channels.values():
            print(value)

        game_main_channel = self.channels["掲示板"]
        join_emoji = EMOJI["join"]
        finish_emoji = EMOJI["finish"]
        self.command.addSendEmoji(game_main_channel, [join_emoji, finish_emoji])
        await self.connecter.Send(
            game_main_channel,
            "人狼ゲームを行います。参加する場合は{}を押してください。\n\n人数が揃ったら、{}を押してください。"\
                .format(join_emoji, finish_emoji)
            )


    


