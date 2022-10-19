import unittest
from parameterized import parameterized
from unittest.mock import patch
from main.consoleGame import *
from main.fourInLine import *

class ConsoleGameDefPlay(unittest.TestCase):

    def setUp(self):
        self.game = Game()

    @parameterized.expand(('exit','Exit','EXIT')) 
    def test_exit(self, parameter):
        with self.assertRaises(ExitGame):
            self.game.defPlay(parameter)
    
    @parameterized.expand(('reset', 'Reset', 'RESET'))
    @patch('main.fourInLine.FourInLine.resetBoard')
    def test_reset(self, parameter, resetBoard):
        self.assertEqual(self.game.defPlay(parameter), '')
        self.assertTrue(resetBoard.called)

    @parameterized.expand(('1', '2', '3', '4', '5', '6', '7', '8'))
    @patch('main.fourInLine.FourInLine.insertToken')
    def test_insertToken(self, parameter, insertToken):
        self.assertEqual(self.game.defPlay(parameter), '')
        self.assertTrue(insertToken.called)

    @parameterized.expand(('es', 'Y', 'YE', '80', '22','2odkd9','exi','¡1¿')) 
    def test_unrecognizedValueOrString(self, parameter):
        with self.assertRaises(FormatException):
            self.game.defPlay(parameter)

    @patch('main.fourInLine.FourInLine.insertToken', side_effect=NoAvailablePositionException)
    def test_noAvailablePosition(self, insertToken):
        self.assertEqual(self.game.defPlay(1), f'\nThere are no more available positions in column 1\n')
        self.assertEqual(self.game.defPlay(2), f'\nThere are no more available positions in column 2\n')

    @patch('main.fourInLine.FourInLine.insertToken', side_effect=TieException)
    @patch('main.fourInLine.FourInLine.resetBoard')
    def test_tie(self, resetBoard, insertToken):
        self.assertEqual(self.game.defPlay(5), '\nTIE! les try again')
        self.assertTrue(resetBoard.called)

    @patch('main.fourInLine.FourInLine.insertToken', side_effect=WinnerException)
    def test_winner(self, insertToken):
        with self.assertRaises(WinnerException):
            self.game.defPlay(1)

class ConsoleGamePlayAgain(unittest.TestCase):

    def setUp(self):
        self.game = Game()

    @patch('builtins.input', return_value='yes')
    def test_inputArgs(self, inputMock):
        self.game.playAgain()
        self.assertEqual(inputMock.call_args.args[0], 'Want to play again?(yes/no)   ')

    @patch('builtins.input', side_effect=['no', 'No', 'NO'])
    def test_exit(self, inputMock):
        for counter in ['no', 'No', 'NO']:
            with self.assertRaises(ExitGame):
                self.game.playAgain()
        self.assertTrue(inputMock.called)

    @patch('builtins.input', side_effect=['yes', 'Yes', 'YES'])
    @patch('main.fourInLine.FourInLine.resetBoard')
    def test_playAgain(self, resetBoard, inputMock):
        for counter in ['yes', 'Yes', 'YES']:
            self.assertEqual(self.game.playAgain(), 'Great, lets go!')
            self.assertTrue(resetBoard.called)

    @patch('builtins.input', side_effect=['es', 'Y', 'YE', '80', '22','2odkd9','exi','¡1¿', 'yes'])
    def test_unrecognizedValueOrString(self, inputMock):
            self.game.playAgain()
            self.assertEqual(inputMock.call_count, len(['es', 'Y', 'YE', '80', '22','2odkd9','exi','¡1¿', 'yes']))

class ConsolePlay(unittest.TestCase):

    def setUp(self):
        self.game = Game()

    @patch('test.test_consoleGame.Game.printBoard', return_value='.printBoard()')
    @patch('test.test_consoleGame.Game.defPlay', return_value='.defPlayStatement')
    @patch('main.fourInLine.FourInLine.returnTurn', return_value=4)
    @patch('builtins.print')
    @patch('builtins.input', side_effect=['userInput', ExitGame])
    def test_firstIterationConditions(self, inputMock, printMock, returnTurn, defPlay, printBoard):
        self.game.play()
        self.assertEqual(str(printMock.call_args_list[0].args[0]), '\nHello lest play Four In Row!')
        self.assertEqual(str(printMock.call_args_list[1].args[0]), '.printBoard()')
        self.assertEqual(inputMock.call_args.args[0], '\nPlayer 5 select a Column(1-8/exit/reset):  ')
        self.assertEqual(str(printMock.call_args_list[2].args[0]), '.printBoard()')
        self.assertEqual(str(printMock.call_args_list[3].args[0]), '.defPlayStatement')
        self.assertEqual(inputMock.call_args.args[0], '\nPlayer 5 select a Column(1-8/exit/reset):  ')

    @patch('test.test_consoleGame.Game.printBoard', return_value='.printBoard()')
    @patch('test.test_consoleGame.Game.defPlay', side_effect=[WinnerException, ExitGame])
    @patch('main.fourInLine.FourInLine.returnTurn', return_value=4)
    @patch('builtins.print')
    @patch('builtins.input', side_effect=['userInput', 'adsa', 'yes', 'userInput'])
    def test_winnerAndPlayAgainConditions(self, inputMock, printMock, returnTurn, defPlay, printBoard):
        self.game.play()
        self.assertEqual(str(printMock.call_args_list[2].args[0]), '.printBoard()') 
        self.assertEqual(str(printMock.call_args_list[3].args[0]), '\nPlayer 5 winns!!!\n')
        self.assertEqual(str(inputMock.call_args_list[1].args[0]), 'Want to play again?(yes/no)   ')
        self.assertEqual(str(inputMock.call_args_list[2].args[0]), 'Want to play again?(yes/no)   ')
        self.assertEqual(str(printMock.call_args_list[4].args[0]), 'Great, lets go!')
        self.assertEqual(str(printMock.call_args_list[5].args[0]), '.printBoard()')
        self.assertEqual(str(inputMock.call_args_list[3].args[0]), '\nPlayer 5 select a Column(1-8/exit/reset):  ')

    @patch('test.test_consoleGame.Game.printBoard', return_value='.printBoard()')
    @patch('test.test_consoleGame.Game.defPlay', side_effect=[FormatException, ExitGame])
    @patch('main.fourInLine.FourInLine.returnTurn', return_value=4)
    @patch('builtins.print')
    @patch('builtins.input', return_value='incorrectUserInput')
    def test_formatExceptionRepeatsMainQuestionConditions(self, inputMock, printMock, returnTurn, defPlay, printBoard):
        self.game.play()
        self.assertEqual(str(inputMock.call_args_list[0].args[0]), '\nPlayer 5 select a Column(1-8/exit/reset):  ')
        self.assertEqual(str(inputMock.call_args_list[1].args[0]), '\nPlayer 5 select a Column(1-8/exit/reset):  ')
        self.assertEqual(printMock.call_count, 2)

    @patch('test.test_consoleGame.Game.printBoard', return_value='.printBoard()')
    @patch('test.test_consoleGame.Game.defPlay', side_effect=WinnerException)
    @patch('main.fourInLine.FourInLine.returnTurn', return_value=4)
    @patch('builtins.print')
    @patch('builtins.input', side_effect=['userInput', 'adsa', 'no'])
    def test_PlayAgain_Exit_Conditions(self, inputMock, printMock, returnTurn, defPlay, printBoard):
        self.game.play()
        self.assertEqual(str(inputMock.call_args_list[0].args[0]), '\nPlayer 5 select a Column(1-8/exit/reset):  ')
        self.assertEqual(printMock.call_count, 4)
        self.assertEqual(inputMock.call_count, 3)

        
class ConsolePrintBoard(unittest.TestCase):

    def setUp(self):
        self.game = Game()

    @patch('main.fourInLine.FourInLine.returnBoard', return_value=
        [['', '', '', '', '', '', '', ''],
        ['', '', '', '', '', '', '', ''], 
        ['', '', '', '', '', '', '', ''], 
        ['', '', '', '', '', '', '', ''], 
        ['', '', '', '', '', '', '', ''], 
        ['', '', '', '', '', '', '', ''], 
        ['', '', '', '', '', '', '', ''], 
        ['', '', '', '', '', '', '', '']])
    def test_defaultPrint(self, fourInLine):
        self.assertEqual(self.game.printBoard(),'\n'
            '  1    2    3    4    5    6    7    8  \n'
            '+----+----+----+----+----+----+----+----+\n'
            '|    |    |    |    |    |    |    |    |\n'
            '+----+----+----+----+----+----+----+----+\n'
            '|    |    |    |    |    |    |    |    |\n'
            '+----+----+----+----+----+----+----+----+\n'
            '|    |    |    |    |    |    |    |    |\n'
            '+----+----+----+----+----+----+----+----+\n'
            '|    |    |    |    |    |    |    |    |\n'
            '+----+----+----+----+----+----+----+----+\n'
            '|    |    |    |    |    |    |    |    |\n'
            '+----+----+----+----+----+----+----+----+\n'
            '|    |    |    |    |    |    |    |    |\n'
            '+----+----+----+----+----+----+----+----+\n'
            '|    |    |    |    |    |    |    |    |\n'
            '+----+----+----+----+----+----+----+----+\n'
            '|    |    |    |    |    |    |    |    |\n'
            '+----+----+----+----+----+----+----+----+\n')

    @patch('main.fourInLine.FourInLine.returnBoard', return_value=
        [['', '', '', '', '', '', 1, ''],
        ['', 0, '', '', '', '', '', ''], 
        ['', '', '', '', '', '', 0, ''], 
        ['', '', '', '', '', '', '', ''], 
        ['', '', 1, '', '', '', '', ''], 
        ['', '', '', '', '', '', '', ''], 
        ['', '', '', '', '', '', '', ''], 
        [1, '', '', '', 0, '', '', '']])
    def test_genericPrint(self, fourInLine):
        self.assertEqual(self.game.printBoard(),'\n'
            '  1    2    3    4    5    6    7    8  \n'
            '+----+----+----+----+----+----+----+----+\n'
            '|    |    |    |    |    |    | 🔵 |    |\n'
            '+----+----+----+----+----+----+----+----+\n'
            '|    | 🔴 |    |    |    |    |    |    |\n'
            '+----+----+----+----+----+----+----+----+\n'
            '|    |    |    |    |    |    | 🔴 |    |\n'
            '+----+----+----+----+----+----+----+----+\n'
            '|    |    |    |    |    |    |    |    |\n'
            '+----+----+----+----+----+----+----+----+\n'
            '|    |    | 🔵 |    |    |    |    |    |\n'
            '+----+----+----+----+----+----+----+----+\n'
            '|    |    |    |    |    |    |    |    |\n'
            '+----+----+----+----+----+----+----+----+\n'
            '|    |    |    |    |    |    |    |    |\n'
            '+----+----+----+----+----+----+----+----+\n'
            '| 🔵 |    |    |    | 🔴 |    |    |    |\n'
            '+----+----+----+----+----+----+----+----+\n')