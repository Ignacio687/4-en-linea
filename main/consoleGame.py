from operator import truediv
from sys import excepthook
from turtle import exitonclick
from main.fourInLine import *

class AskAgain(Exception):
    pass

class ExitGame(Exception):
    pass

class Game():

    def __init__(self):
        self.game = FourInLine()
        self.gameState = 0

    def play(self):
        print('\nHello lest play Four In Row!')
        print(self.printBoard())
        while True:
            try:
                consoleInput = input(f'\nPlayer {self.game.returnTurn()+1} select a Column(1-8/exit/reset):  ')
                statement = self.defPlay(consoleInput)
                print(self.printBoard())
                print(statement)
            except FormatException:
                continue
            except ExitGame:
                break
            except WinnerException:
                print(f'\nPlayer {self.game.returnTurn()+1} winns!!!\n')
                try:
                    print(self.playAgain())
                    print(self.printBoard())
                except ExitGame:
                    break

    def defPlay(self, playerInstruction):
        if playerInstruction in ('exit','Exit','EXIT'):
            raise ExitGame
        elif playerInstruction in ('reset', 'Reset', 'RESET'):
            self.game.resetBoard()
            returnStatement = ''
        else:
            try:
                self.game.insertToken(int(playerInstruction)-1)
                returnStatement = ''
            except (OutOfRangeException, FormatException, ValueError):
                raise FormatException
            except NoAvailablePositionException:
                returnStatement = f'\nThere are no more available positions in column {playerInstruction}\n'
            except TieException:
                self.game.resetBoard()
                returnStatement = '\nTIE! les try again'
            except WinnerException:
                raise WinnerException
        return returnStatement

    def playAgain(self):
        while True:
            playerInstruction = input('Want to play again?(yes/no)   ')
            if playerInstruction in ('no', 'No', 'NO'):
                    raise ExitGame
            elif playerInstruction in ('yes', 'Yes', 'YES'):
                    self.game.resetBoard()
                    return 'Great, lets go!'

    def printBoard(self):
        board = self.game.returnBoard()
        printingBoard='\n'
        for line in range(1, len(board)+1):
            printingBoard += f'  {line}  '
        printingBoard +='\n+'+('----+'*len(board)+'\n')
        for line in range(0, len(board)):
            for row in range(0, len(board[line])):
                if board[line][row] != '':
                    printValue = ' 🔴 ' if board[line][row] == 0 else ' 🔵 '
                else:
                    printValue = '    '
                printingBoard += f'|{printValue}'
            printingBoard += '|\n+'+('----+'*len(board)+'\n')
        return printingBoard