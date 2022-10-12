from main.game import *

class ExitGame(Exception):
    pass

class Game():

    def __init__(self):
        self.game = FourInRow()
        self.printStatement = f'\nPlayer {(self.game.turn)+1} select a Column(1-8/exit/reset):  '

    def play(self):
        print('\nHello lest play Four In Row!')
        self.printBoard()
        while True:
            try:
                consoleInput = input(self.printStatement)
                instructions = self.print_input(consoleInput)
                self.printBoard()
                print(instructions)
            except ExitGame:
                break

    def print_input(self, playerInstruction):
        returnStatement = ''
        if 'again' in self.printStatement:
            if playerInstruction in ('no', 'No', 'NO'):
                raise ExitGame
            elif playerInstruction in ('yes', 'Yes', 'YES'):
                self.printStatement = f'\nPlayer {(self.game.turn)+1} select a Column(1-8/exit/reset):  '
                self.game.resetBoard()
        else:
            if playerInstruction in ('exit','Exit','EXIT'):
                raise ExitGame
            elif playerInstruction in ('reset', 'Reset', 'RESET'):
                self.game.resetBoard()
            else:
                try:
                    self.game.insertToken(int(playerInstruction)-1)
                except (OutOfRangeException, formatException, ValueError):
                    returnStatement = ''
                except NoAvailablePositionException:
                    returnStatement = f'\nThere are no more available positions in column {playerInstruction}\n'
                except TieException:
                    self.game.resetBoard()
                    returnStatement = '\nTIE! les try again'
                except WinnerException:
                    self.printStatement = 'Want to play again?(yes/no)  '
                    returnStatement = f'\nPlayer {self.game.turn+1} winns!!!\n'
        return returnStatement
                    
    def printBoard(self):
        board = self.game.board
        print('\n')
        for line in range(1, len(board)+1):
            print(f'  {line}  ', end='')
        print('\n+'+('----+'*len(board)))
        for line in range(0, len(board)):
            for row in range(0, len(board[line])):
                if board[line][row] != '':
                    printValue = ' 🔴 ' if board[line][row] == 0 else ' 🔵 '
                else:
                    printValue = '    '
                print (f'|{printValue}', end='')
            print('|\n+'+('----+'*len(board)))