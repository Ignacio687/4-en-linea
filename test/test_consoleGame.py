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