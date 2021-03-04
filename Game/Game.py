BASIC_CREATE_TEXT_CHANNELS_NAME = [
    "人狼の会合",
    "霊界",
    "掲示板"
]

BASIC_CREATE_VOICE_CHANNELS_NAME = [
    "討論場"
]

GAME_MINIMUM_PLAYER_NUM = 1


from discord.ext import tasks
from System.Command import EMOJI
from Game.Player import *
from Game.GameRule import *
import enum
import random

# フェーズ
class Phase(enum.Enum):
    NON_GAME = 0,
    START = 1,
    MORNING = 2,
    DISCUSSION = 3, 
    VOTE = 4,
    NIGHT = 5,
    FIRST_NIGHT = 6

# ゲーム
class Game:
    def __init__(self, _connecter, _command):
        # プレイヤー一覧(alive：生存、dead:死亡)
        self.players = []
        self.num_player = 0
        self.alive = []
        self.dead = []

        self.rule = GameRule()

        # 現在の日数
        self.now_day = 0

        # 現在の議論時間
        self.now_pass_time = 0

        # 議論の最大時間
        self.max_discuss_time = 1

        # システム関係
        self.connecter = _connecter
        self.command = _command

        # カテゴリ、チャンネル系
        self.use_category = None
        self.channels = {}

        # 現在ゲームを実行中かどうか
        self.is_game = False

        # フェーズタイプを設定する。
        self.phase = Phase.NON_GAME

        # 既にタイマーを起動しているかどうか
        self.is_run_timer = False


    # ゲーム開始時の初期化
    def GameInit(self):
        self.alive = self.players
        self.dead = []
        self.phase = Phase.NON_GAME
        self.now_pass_time = 0


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


    @tasks.loop(minutes=1)
    async def TimerDiscussion(self):
        await self.connecter.Reply("@everyone", self.channels["掲示板"], "タイマー開始")
        if self.now_pass_time > 0:
            await self.connecter.Reply("@everyone", self.channels["掲示板"], "{}分経過しました".format(self.now_pass_time))

        self.now_pass_time += 1

        if self.now_pass_time > self.max_discuss_time:
            await self.onVote()

    async def ForceMuteAlivePlayer(self):
        for player in self.alive:
            await self.connecter.SetMute(player.user, True)
        
    async def DismuteAlivePlayer(self):
        for player in self.alive:
            await self.connecter.SetMute(player.user, False)

    
    # ゲーム開始によって呼び出される処理
    async def onRecruitment(self, message):
        if self.is_game:
            await self.connecter.Reply(message.author.mention, message.channel, "現在ゲームを開催中です。\n!game_finishで終了してから再度実行してください。")
            return

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
                await self.onStart()
        self.command.addStackMethod(game_main_channel, do, message=dialog_message)


    async def onFinish(self, message):
        if not self.is_game:
            return
        await self.connecter.Reply("@everyone", self.channels["掲示板"], "ゲームを終了しました")
        self.AllReset()
        self.TimerDiscussion.cancel()
        self.is_run_timer = False


    # 役職の割り当て
    # @param is_lack: 役欠けありか
    def AssignRole(self, is_lack):
        # 役欠けありなら割り当て対象にGMを選択
        if is_lack:
            self.players.append(
                Player("GM", 1000)
            )
        shuffled = random.shuffle(self.players)
        for i in range(self.players):
            role_tag = self.rule.AssignRole(i)

            # 役職が見つからないなら、エラーを出して終了
            if role_tag == None:
                await self.connecter.Reply("@everyone", self.channels["掲示板"], "役職の総数が足りていません")
                await self.onFinish()

            self.players[i].setRole(role_tag)



    async def onStart(self):
        # todo : 役職の通知
        # todo : 人狼が割り当てられた人は人狼チャットの閲覧権限を付与
        
        await self.ForceMuteAlivePlayer()

        self.phase = Phase.START
        await self.connecter.Reply("@everyone", self.channels["掲示板"], "ゲームを開始します。")

        # 役職の割り当て
        self.AssignRole(self.rule.is_role_lack)

        await self.onFirstNight()


    async def onFirstNight(self):
        # todo : 全ての人の夜の行動を実行
        # todo : 全て完了してから、朝に移行
        # todo : 占い師の初夜占いは設定を変更する。
        self.phase = Phase.FIRST_NIGHT
        await self.connecter.Reply("@everyone", self.channels["掲示板"], "初夜の行動を行います。")
        await self.onMorning()

    # 朝のフェーズ
    async def onMorning(self):
        # todo : 朝の能力がある役職はここで
        # todo : 夜の死亡者を通知
        # todo : 勝敗判定を行う
        for player in self.alive:
            self.connecter.SetMute(player.user, True)

        self.phase = Phase.MORNING
        await self.connecter.Reply("@everyone", self.channels["掲示板"], "朝のフェーズになりました。")
        await self.onDiscussion()


    # 議論フェーズ
    async def onDiscussion(self):
        self.phase = Phase.DISCUSSION
        await self.DismuteAlivePlayer()

        await self.connecter.Reply("@everyone", self.channels["掲示板"], "議論のフェーズになりました。")
        if self.is_run_timer:
            self.TimerDiscussion.restart()
        else:
            self.is_run_timer = True
            self.TimerDiscussion.start()


    # 投票フェーズ
    async def onVote(self):
        # todo : 投票シンボルを各プレイヤーに送信
        # todo : 投票が完了したら、最も多かった人を追放する
        # todo : 最多得票数の人が複数人いたら、決選投票
        # todo : 勝敗判定
        # todo : 遺言があるなら、追放された人だけミュートを解除する。
        # todo : 死亡者には霊界チャットの閲覧権限を付与
        self.phase = Phase.VOTE

        await self.ForceMuteAlivePlayer()


        # タイマー関連の変数をリセットする
        self.TimerDiscussion.stop()
        self.now_pass_time = 0

        await self.connecter.Reply("@everyone", self.channels["掲示板"], "投票の時間になりました")
        await self.onNight()


    # 夜フェーズ
    async def onNight(self):
        # todo : 夜の能力がある人のものを使用する。
        # todo : 他の人は、疑わしい人に関しての質問を行う
        # todo : 全員が完了してから、実行結果を全員に通知する。
        # todo : 死亡者には霊界チャットの閲覧権限を付与
        self.phase = Phase.NIGHT
        await self.connecter.Reply("@everyone", self.channels["掲示板"], "夜のフェーズになりました。")
        await self.onMorning()
