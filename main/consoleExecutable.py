import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from main.game import *

class Game():

    def __init__(self):
        self.game = FourInRow()

    def play(self):
        print('Hello lest play Four In Row! \n\n')
        gameStatus = False
        while not gameStatus:
            self.printBoard()
            playerInstruction = input(f'\nPlayer {(self.game.turn)+1} select a Column(1-8/exit/reset):  ')
            if playerInstruction in ('exit','Exit','EXIT'):
                break
            elif playerInstruction in ('reset', 'Reset', 'RESET'):
                self.game.resetBoard()
            else:
                try:
                    self.game.insertToken(int(playerInstruction)-1)
                except (OutOfRangeException, formatException, ValueError):
                    continue
                except NoAvailablePositionException:
                    print(f'\nTheres no more available positions in column {playerInstruction}\n')
                except TieException:
                    print('TIE! les try again')
                    self.game.resetBoard()
                except WinnerException:
                    self.printBoard()
                    print(f'\nPlayer {self.game.turn+1} winns!!!\n')
                    while True:
                        playerInstruction = input('Want to play again?(yes/no)  ')
                        if  playerInstruction in ('yes', 'Yes', 'YES'):
                            self.game.resetBoard()
                            break
                        elif playerInstruction in ('no', 'No', 'NO'):
                            gameStatus = True
                            break
                    
    def printBoard(self):
        board = self.game.board
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

if __name__=='__main__':
    game = Game()
    game.play()