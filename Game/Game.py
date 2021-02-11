BASIC_CREATE_TEXT_CHANNELS_NAME = [
    "人狼の会合",
    "霊界",
    "掲示板"
]

BASIC_CREATE_VOICE_CHANNELS_NAME = [
    "討論場"
]

GAME_MINIMUM_PLAYER_NUM = 1


from System.Command import EMOJI
from Game.Player import *

class Game:
    def __init__(self, _connecter, _command):
        # プレイヤー一覧(alive：生存、dead:死亡)
        self.players = []
        self.num_player = 0
        self.alive = []
        self.dead = []

        # 現在の日数
        self.now_day = 0

        # 役職表
        self.role_table = {}

        # システム関係
        self.connecter = _connecter
        self.command = _command

        # カテゴリ、チャンネル系
        self.use_category = None
        self.channels = {}

        # 現在ゲームを実行中かどうか
        self.is_game = False


    # ゲーム開始時の初期化
    def GameInit(self):
        self.alive = self.players
        self.dead = []
        self.role_table = {}


    # 完全リセット
    def AllReset(self):
        self.is_game = False
        self.players = []
        self.num_player = 0
        self.use_category = None
        self.channels = {}
        self.GameInit()
    

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

    
    # プレイヤーの追加
    def AddPlayer(self, member):
        self.players.append(
            Player(member, self.num_player)
        )
        self.num_player += 1

    # プレイヤーの削除
    def RemovePlayer(self, member):
        remove_player = None
        for player in self.players:
            if player.mention == member.mention:
                remove_player = player
                break
        if remove_player == None:
            return
        self.players.remove(remove_player)
        self.num_player -= 1


    
    # ゲーム開始によって呼び出される処理
    async def onStart(self, message):
        # if self.is_game:
        #     await self.connecter.Reply(message.author.mention, message.channel, "現在ゲームを開催中です。\n!game_finishで終了してから再度実行してください。")
        #     return

        # ゲームで使用するカテゴリの作成
        self.use_category = await self.GetCategory("人狼ゲーム")

        # 基本的に使用するチャンネルを取得
        await self.GetTextChannels(BASIC_CREATE_TEXT_CHANNELS_NAME)
        await self.GetVoiceChannels(BASIC_CREATE_VOICE_CHANNELS_NAME)

        await self.connecter.Reply(message.author.mention, message.channel, "{}で参加者を募ります".format("掲示板"))

        game_main_channel = self.channels["掲示板"]
        join_emoji = EMOJI["join"]
        finish_emoji = EMOJI["finish"]
        self.command.addSendEmoji(game_main_channel, [join_emoji, finish_emoji])
        dialog_message = await self.connecter.Send(
            game_main_channel,
            "人狼ゲームを行います。参加する場合は{}を押してください。\n\n人数が揃ったら、{}を押してください。"\
                .format(join_emoji, finish_emoji)
            )
        
        async def do(payload):
            if payload.emoji.name == EMOJI["join"]:
                member = self.connecter.GetUser(payload.user_id)
                if payload.event_type == "REACTION_ADD":
                    self.AddPlayer(member)
                else:
                    self.RemovePlayer(member)
            elif payload.emoji.name == EMOJI["finish"]:
                await self.command.InitStackMethod(game_main_channel)
                if self.num_player < GAME_MINIMUM_PLAYER_NUM:
                    await self.connecter.Send(game_main_channel, "人数が不足しているためゲームを開始できません。\n{}人以上必要です。".format(GAME_MINIMUM_PLAYER_NUM))
                    return
                self.is_game = True
                members = ""
                for p in self.players:
                    members += "{}\n".format(p.mention)
                await self.connecter.Send(game_main_channel, "以下の{}人でゲームを行います\n{}".format(self.num_player, members))
                self.GameInit()
        self.command.addStackMethod(game_main_channel, do, message=dialog_message)


    async def onFinish(self, message):
        if not self.is_game:
            return
        await self.connecter.Reply("@everyone", self.channels["掲示板"], "ゲームを終了しました")
        self.AllReset()



