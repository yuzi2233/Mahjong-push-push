from Mahjong import *
import random


class ChessBoard:
    def __init__(self,player):

        self.mahjongs = []
        self.first_player_board = []
        self.second_player_board = []
        self.next_MJ=Mahjong('Dot', 1)
        self.use_board=[]
        self.player=player
        self.counter=[[4,4,4,4,4,4,4,4,4],[4,4,4,4,4,4,4,4,4]]
    '''
    发牌程序
    '''

    def dealCard(self):
        chess_forms = ['Dot', 'Bamboo']

        for i in range(1, 10):
            for j in range(4):
                chess = Mahjong('Dot', i)
                self.mahjongs.append(chess)

        for i in range(1, 10):
            for j in range(4):
                chess = Mahjong('Bamboo', i)
                self.mahjongs.append(chess)
        random.shuffle(self.mahjongs)  # 洗牌

        half = int(len(self.mahjongs) / 2)  # 分堆
        first_heap = self.mahjongs[:half]
        second_heap = self.mahjongs[half:]

        k = 0
        for i in range(9):
            tmp = []
            for j in range(4):
                tmp.append(first_heap[k])
                k = k + 1
            self.first_player_board.append(tmp)

        k = 0
        for i in range(9):
            tmp = []
            for j in range(4):
                tmp.append(second_heap[k])
                k = k + 1
            self.second_player_board.append(tmp)

    '''
    推出一个的棋子
    '''

    def pushChess(self, idx, player):

        if player == 1:
            self.use_board = self.first_player_board
        else:
            self.use_board = self.second_player_board

        if not self.checkLineIsNotFull(idx, player):
            return

        self.getFirstMj(idx,player)



    def addChess(self, idx,player):

        if not self.checkLineIsNotFull(idx, player):
            return
        self.use_board[idx-1][0]=self.next_MJ



    def setNextPlayer(self):
        if self.next_MJ.form=='Dot':
            self.player=0
        else:
            self.player=1

    def checkLineIsNotFull(self, idx,player):
        if self.counter[player][idx-1] == 0 :
            return False
        else:
            return True
        pass

    '''
    获取idx列中最顶端的麻将
    '''
    def getFirstMj(self, idx,player):
        self.next_MJ=self.use_board[idx-1][4]
        self.next_MJ.status = 1  # 翻面
        self.counter[player][idx-1]=self.counter[player][idx-1] - 1
        self.use_board[idx-1][3]=self.use_board[idx-1][2]
        self.use_board[idx - 1][2] = self.use_board[idx - 1][1]
        self.use_board[idx - 1][1] = self.use_board[idx - 1][0]


    def throwError(self):
        pass

chess_board = ChessBoard()
chess_board.dealCard()
for i in range(9):
    for j in range(4):
        print(chess_board.first_player_heap[i][j].form + " " + str(chess_board.first_player_heap[i][j].num))
