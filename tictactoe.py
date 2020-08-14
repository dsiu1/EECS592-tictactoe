import os
import random
import sys
import math


class tttboard():
    def __init__(self, board=['-' for i in range(0, 9)]):
        # self.board = ['o','-','-',\
        #               'x','-','x',\
        #               'o','-','-']
        self.board = board
        self.moves = 0
        self.totalmoves = 0
        self.existspace = [i for i in range(0, 9) if (self.board[i] == '-')]
        self.scores = [-1000 for i in range(0, len(self.existspace))]
        self.bestindex = 0

    def movesLeft(self):
        return [i for i in range(0, 9) if (self.board[i] == '-')]

    def scoresLeft(self):
        return [-1000 for i in range(0, len(self.existspace))]

    def checkWinner(self, player):
        ##Check vertical
        for i in [0, 1, 2]:
            if (self.board[i] == player and self.board[i + 3] == player and self.board[i + 6] == player):
                return True
        ##Check horizontal
        for i in [0, 3, 6]:
            if (self.board[i] == player and self.board[i + 1] == player and self.board[i + 2] == player):
                return True

        ##Check cross
        if ((self.board[0] == player and self.board[4] == player and self.board[8] == player) or
                (self.board[2] == player and self.board[4] == player and self.board[6] == player)):
            return True
        return False

    def addChoice(self, position, player):
        self.board[position] = player

    def filled(self, position):
        movesLeft = self.movesLeft()
        try:
            ind = movesLeft.index(position)
            return False
        except:
            return True

    def displayBoard(self):
        print(self.board[6] + ',' + self.board[7] + ',' + self.board[8])
        print(self.board[3] + ',' + self.board[4] + ',' + self.board[5])
        print(self.board[0] + ',' + self.board[1] + ',' + self.board[2])
        print("")


def minimax(board, player, height):
    if (board.checkWinner('x')):
        return 10 - height

    elif (board.checkWinner('o')):
        return -10 + height
    elif (len(board.movesLeft()) < 1):

        return 0
    ##Recording height to weight the boards properly
    ##Boards which have more plays should be less preferred. A board that wins immediately is preferred.
    ##Perhaps we need to do the reverse weighting for x win conditions

    board.totalmoves += 1

    ##Minimizing
    if (player == 'o'):
        bestval = 1000  ##Initialize bestval
        movesLeft = board.movesLeft()
        board.scores = board.scoresLeft()
        for i in range(0, len(movesLeft)):

            ##Placing a piece, then updating the board and existing space
            move = movesLeft[i]
            board.board[move] = player
            board.bestindex = move

            ##Recursively call minimax on next player
            minval = minimax(board, 'x', height + 1)
            ##Append to index and value list here, then outside the loop we evaluate the best index?
            if (minval < bestval):
                bestval = minval
                board.bestindex = move

            ##Reset board, and append scores to each of the moves
            board.board[move] = '-'
            try:
                board.scores[move] = bestval
            except:
                L = 1

            board.moves -= 1

        ##After you reach the bottom of the finished board, we look for the lowest score, which indicates o would win
        ##The index is also returned so that we can place the piece
        return bestval


    ##Maximizing. See comments above for the same logic.
    elif (player == 'x'):
        bestval = -1000  ##Initializing bestvalue
        movesLeft = board.movesLeft()
        board.scores = board.scoresLeft()
        for i in range(0, len(movesLeft)):

            move = movesLeft[i]
            board.board[move] = player

            maxval = minimax(board, 'o', height + 1)
            if (maxval > bestval):
                bestval = maxval
                board.bestindex = move

            board.board[move] = '-'

            try:
                board.scores[move] = bestval
            except:
                L = 1

        return bestval


if __name__ == '__main__':
    print
    s = int(input("Enter a seed number: "))
    "Seed = ", s
    random.seed(s);
    tictactoe = tttboard()
    index = 0

    ##Continue to run the algorithm and display the next board until somebody wins
    while (not (tictactoe.checkWinner('x')) and not (tictactoe.checkWinner('o'))):

        nextpos = math.floor(9 * random.random())

        while (tictactoe.filled(nextpos)):
            nextpos = math.floor(9 * random.random())
        tictactoe.addChoice(int(nextpos), 'x')
        if not tictactoe.existspace:
            break
        bestval = minimax(tictactoe, 'o', 1)
        bestindex = tictactoe.scores.index(max(tictactoe.scores))
        tictactoe.addChoice(int(tictactoe.bestindex), 'o')
        tictactoe.displayBoard()



    ##Player 1 should  be random

    ##Player 2 should be minimax

    ##Board is
    ## 0 1 2
    ## 3 4 5
    ## 6 7 8