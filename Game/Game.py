from discord.ext import tasks
from System.Command import EMOJI
from Game.Player import *
from Game.GameRule import *
import enum
import random

# チャットの名前を定義する
MAIN_CHAT_NAME = "掲示板"           # メインのテキストチャット
WAREWOLF_CHAT_NAME = "人狼の会合"   # 人狼用の共通チャット
DEAD_PLAYER_CHAT_NAME = "霊界"      # 死亡者用の共通チャット

VOICE_CHAT_NAME = "討論場"          # 議論で使用する音声チャット

# 共通で使用するテキストチャット
BASIC_CREATE_TEXT_CHANNELS_NAME = [
    WAREWOLF_CHAT_NAME,
    DEAD_PLAYER_CHAT_NAME,
    MAIN_CHAT_NAME
]

# 共通で使用する音声チャット
BASIC_CREATE_VOICE_CHANNELS_NAME = [
    VOICE_CHAT_NAME
]

# ゲームを開始する最小人数
GAME_MINIMUM_PLAYER_NUM = 1

EVERYONE_MENTION = "@everyone"


# フェーズ
class Phase(enum.Enum):
    NON_GAME = 0,
    START = 1,
    MORNING = 2,
    DISCUSSION = 3, 
    VOTE = 4,
    EXPULSION = 5,
    EVENING = 6,
    NIGHT = 7,
    FIRST_NIGHT = 8

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
        self.max_discuss_time = 0

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

        # アクションスタック
        self.action = {}
        self.action_count = 0
        self.action_wait_time = 0
        self.is_run_action_wait = False

        # 投票リストの初期化
        self.vote_count = []

        # 決選投票の投票先になっているプレイヤー
        self.final_voted_player = None


    # ゲーム開始時の初期化
    def GameInit(self):
        self.alive = self.players
        self.dead = []
        self.phase = Phase.NON_GAME
        self.now_pass_time = 0
        self.action_count = 0
        self.action_wait_time = 0
        self.is_run_action_wait = False
        self.vote_count = []
        self.final_voted_player = None


    # 完全リセット
    def AllReset(self):
        self.is_game = False
        self.players = []
        self.num_player = 0
        self.use_category = None
        self.channels = {}
        self.action = {}
        self.GameInit()

    
    # 生存者から一人を選ばせるメッセージを投げる。
    async def SendSelectMessage(self, target, purpose, select_list):
        sentence = purpose + "\n数字で選択して、メッセージで送信してください\n\n"
        ind = 0
        for player in select_list:
            if player != target:
                ind += 0
                sentence += "[{}] : {}\n".format(ind, player.name)
        
        await self.connecter.Send(self.GetPlayerChannel(target), sentence)
    

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

    
    # プレイヤーから、チャンネルを検索する
    def GetPlayerChannel(self, player):
        return self.channels[player.name]

    
    # channelからプレイヤーを特定して、Actionを実行する
    async def CheckAction(self, member, number):
        if self.phase == Phase.DISCUSSION:
            return

        # 決選投票以外では、リストから投票者が除外されているため、それを考慮したインデックスに変換する必要がある
        # 決選投票は、投票対象プレイヤーが投票できないため、考慮する必要がない
        if self.final_voted_player == None:
            # numberがメンバーのインデックス以上ならその分増加する
            ind = -1
            for i, player in enumerate(self.alive):
                if player.name == member:
                    ind = i
            
            # 生存者リストに見つからないなら終了
            if ind == -1:
                print("CheckActionで、生存者リストに該当者が見つかりません")
                return
            
            if number >= ind:
                number += 1

        if number > len(self.alive) or number < 0:
            await self.connecter.Send(self.channels[member], "対象プレイヤーの数字を正確に入力してください")
            return

        # アクションの実行
        if self.action[member] != None:
            self.action[member](number)
            self.action[member] = None
            self.action_count += 1
        

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

    
    # プレイヤーの追放
    async def Expulsion(self, index):
        # 対象プレイヤーを生存プレイヤーから取り出す
        print("expulsion {} player".format(index))
        if self.final_voted_player != None:
            expulsion_target = self.alive.pop(self.final_voted_player[index])
        else:
            expulsion_target = self.alive.pop(index)

        # 対象プレイヤーを死亡プレイヤーに追加
        self.dead.append(expulsion_target)

        # 霊界チャットの権限を付与する
        await self.connecter.SetTextChannelPermission(self.channels[DEAD_PLAYER_CHAT_NAME], expulsion_target.user, read=False, send=False, reaction=False, read_history=False)


    # 議論時間の管理
    @tasks.loop(minutes=1)
    async def TimerDiscussion(self):
        await self.connecter.Reply(EVERYONE_MENTION, self.channels[MAIN_CHAT_NAME], "タイマー開始")
        if self.now_pass_time > 0:
            await self.connecter.Reply(EVERYONE_MENTION, self.channels[MAIN_CHAT_NAME], "{}分経過しました".format(self.now_pass_time))

        self.now_pass_time += 1

        if self.now_pass_time > self.max_discuss_time:
            await self.onVote()

    
    # アクションの待機
    @tasks.loop(seconds=1)
    async def WaitAction(self):

        if self.final_voted_player == None:
            num_action_user = len(self.alive)
        else:
            num_action_user = len(self.alive) - len(self.final_voted_player)

        if self.action_count == num_action_user:
            # 投票アクション
            if self.phase == Phase.VOTE:
                await self.onExpulsion()

            # 初夜のアクション
            elif self.phase == Phase.FIRST_NIGHT:
                await self.onMorning()

            # 夜のアクション
            elif self.phase == Phase.NIGHT:
                await self.onMorning()
        
        self.action_wait_time += 1

        # 三分ごとにリマインドする
        if self.action_wait_time % (3 * 60) == 0:
            await self.connecter.Send(self.channels[MAIN_CHAT_NAME], "行動が完了していません。\n個人用チャンネルで対象プレイヤーを数字で選択してください。")


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

        await self.connecter.Reply(message.author.mention, message.channel, "{}で参加者を募ります".format(MAIN_CHAT_NAME))

        game_main_channel = self.channels[MAIN_CHAT_NAME]
        join_emoji = EMOJI["join"]
        finish_emoji = EMOJI["finish"]
        self.command.addSendEmoji(game_main_channel, [join_emoji, finish_emoji])
        dialog_message = await self.connecter.Send(
            game_main_channel,
            "人狼ゲームを行います。参加する場合は{}を押してください。\n\n人数が揃ったら、{}を押してください。"\
                .format(join_emoji, finish_emoji)
            )
        
        # スタンプを操作したときに実行する処理
        async def do(payload):
            if payload.emoji.name == EMOJI["join"]:
                member = self.connecter.GetUser(payload.user_id)
                if payload.event_type == "REACTION_ADD":
                    self.AddPlayer(member)
                    # 専用チャンネルを作成
                    await self.GetTextChannels([member.name])
                else:
                    self.RemovePlayer(member)
                    # 使用チャンネルのリストから削除
                    if member.name in self.channels.keys():
                        del self.channels[member.name]
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


    # ゲームの終了処理
    async def onFinish(self):
        if not self.is_game:
            return
        await self.connecter.Reply(EVERYONE_MENTION, self.channels[MAIN_CHAT_NAME], "ゲームを終了しました")
        self.AllReset()
        self.TimerDiscussion.cancel()
        self.is_run_timer = False

    
    async def Finish(self, message):
        await self.onFinish()


    # 役職の割り当て
    # @param is_lack: 役欠けありか
    def AssignRole(self, is_lack):
        # 役欠けありなら割り当て対象にGMを選択
        if is_lack:
            self.players.append(
                Player("GM", 1000)
            )
        shuffled = random.shuffle(self.players)
        for i in range(len(self.players)):
            role_tag = self.rule.AssignRole(i)

            # 役職が見つからないなら、エラーを出して終了
            if role_tag == None:
                return False

            self.players[i].setRole(role_tag)
        return True



    async def onStart(self):
        # 強制ミュート
        await self.ForceMuteAlivePlayer()

        self.phase = Phase.START
        await self.connecter.Reply(EVERYONE_MENTION, self.channels[MAIN_CHAT_NAME], "ゲームを開始します。")

        # 役職の割り当て
        if (not self.AssignRole(self.rule.is_role_lack)):
            # 割り当てに失敗したらエラーを出して終了
            await self.connecter.Reply(EVERYONE_MENTION, self.channels[MAIN_CHAT_NAME], "役職の総数が足りていません")
            await self.onFinish()
        
        # テキストチャットの閲覧権限設定。自分専用のチャンネルと掲示板以外は閲覧不可に設定する
        for player in self.players:
            for key in self.channels.keys():
                if key != MAIN_CHAT_NAME and key != VOICE_CHAT_NAME and key != player.name:
                    await self.connecter.SetTextChannelPermission(self.channels[key], player.user, read=False, send=False, reaction=False, read_history=False)

        # 人狼チャットを見える人を割り当てる
        for player in self.players:
            # 人狼チャットは見える設定の人にだけ見える状態にする。
            if player.role.visible_warewolf_chat:
                await self.connecter.SetTextChannelPermission(self.channels[WAREWOLF_CHAT_NAME], player.user, read=True, send=True, reaction=True, read_history=True)

        # 全プレイヤーの専用チャンネルに役職情報を配布
        for player in self.players:
            await self.connecter.Reply(player.mention, self.GetPlayerChannel(player), player.role.GetExplainText())

        await self.onFirstNight()


    async def onFirstNight(self):
        # todo : 全て完了してから、朝に移行
        # todo : 占い師の初夜占いは設定を変更する。

        for player in self.alive:
            player.onNight(self, is_first=True)

        self.phase = Phase.FIRST_NIGHT
        await self.connecter.Reply(EVERYONE_MENTION, self.channels[MAIN_CHAT_NAME], "初夜の行動を行います。")
        await self.onMorning()

    # 朝のフェーズ
    async def onMorning(self):
        # todo : 夜の死亡者を通知
        # todo : 勝敗判定を行う

        for player in self.alive:
            player.onMorning(self)

        self.phase = Phase.MORNING
        await self.connecter.Reply(EVERYONE_MENTION, self.channels[MAIN_CHAT_NAME], "朝のフェーズになりました。")
        await self.onDiscussion()


    # 議論フェーズ
    async def onDiscussion(self):
        self.phase = Phase.DISCUSSION
        await self.DismuteAlivePlayer()

        await self.connecter.Reply(EVERYONE_MENTION, self.channels[MAIN_CHAT_NAME], "議論のフェーズになりました。")
        if self.is_run_timer:
            self.TimerDiscussion.restart()
        else:
            self.is_run_timer = True
            self.TimerDiscussion.start()


    # 投票フェーズ
    async def onVote(self):
        # todo : 投票シンボルを各プレイヤーに送信
        self.phase = Phase.VOTE

        # 全員を強制ミュートする
        await self.ForceMuteAlivePlayer()

        # タイマー関連の変数をリセットする
        self.TimerDiscussion.stop()
        self.now_pass_time = 0

        await self.connecter.Reply(EVERYONE_MENTION, self.channels[MAIN_CHAT_NAME], "投票の時間になりました")

        # 投票アクションの定義
        def do(index):
            self.vote_count[index] += 1

        # 投票数をカウンティングする
        self.vote_count = [0 for i in range(len(self.alive))]

        # 投票メッセージを生存プレイヤー全員に送信する
        for player in self.alive:
            await self.SendSelectMessage(player, "投票先を選択してください", self.alive)
            self.action[player.name] = do

        # アクションを待機する処理を実行する
        if self.is_run_action_wait:
            self.action_wait_time = 0
            self.WaitAction.restart()
        else:
            self.action_wait_time = 0
            self.WaitAction.start()
            self.is_run_action_wait = True


    async def onExpulsion(self):
        self.phase = Phase.EXPULSION

        self.WaitAction.stop()

        print(self.vote_count)

        # 投票数が最大のプレイヤーのリストを作成する
        max_value = max(self.vote_count)
        max_voted_player = []
        for i, value in enumerate(self.vote_count):
            if value == max_value:
                max_voted_player.append(i)

        # 決選投票でも決まらなかったら、ランダムに一人を選択する
        if self.final_voted_player != None and len(max_voted_player) > 1:
            temp = random.choice(max_voted_player)
            max_voted_player = temp

        if len(max_voted_player) == 1:
            # 生存プレイヤーから除外
            await self.Expulsion(max_voted_player[0])
            self.final_voted_player = None
        else:
            # 決選投票後に同数であったならランダムに追放する
            if self.final_voted_player != None:
                self.connecter.Send(self.channels[MAIN_CHAT_NAME], "決選投票で最高得票のプレイヤーが複数人いました。\nランダムに追放します。")
                expulsion_index = random.choice(max_voted_player)
                self.Expulsion(expulsion_index)

                await self.onEvening()
                return

            # 投票アクションを追加
            def do(index):
                self.vote_count[index] += 1

            self.final_voted_player = max_voted_player

            # 投票数をカウンティングする
            self.vote_count = [0 for i in range(len(max_voted_player))]

            i = 0
            # 決選投票メッセージを生存プレイヤー全員に送信する
            for player in self.alive:
                if not i in max_voted_player:
                    await self.SendSelectMessage(player, "決選投票先を選択してください", [self.alive[ind] for ind in max_voted_player])
                    self.action[player.name] = do
                else:
                    await self.connecter.Send(self.GetPlayerChannel(player), "決選投票中です。お待ちください")
                i += 1
            
            # 投票待機を実行
            self.action_wait_time = 0
            self.WaitAction.restart()
        
        await self.onEvening()


        

        
    async def onEvening(self):
        # todo : 勝敗判定
        # todo : 遺言があるなら、追放された人だけミュートを解除する。
        # todo : 死亡者には霊界チャットの閲覧権限を付与
        self.phase = Phase.EVENING



    # 夜フェーズ
    async def onNight(self):
        # todo : 他の人は、疑わしい人に関しての質問を行う
        # todo : 全員が完了してから、実行結果を全員に通知する。
        # todo : 死亡者には霊界チャットの閲覧権限を付与

        for player in self.alive:
            player.onNight(self)

        self.phase = Phase.NIGHT
        await self.connecter.Reply(EVERYONE_MENTION, self.channels[MAIN_CHAT_NAME], "夜のフェーズになりました。")
        await self.onMorning()
