import unittest
from parameterized import parameterized
from unittest.mock import patch
from main.consoleGame import *

class ExecutableTestCase(unittest.TestCase):

    def setUp(self):
        self.game = Game()

    @parameterized.expand(('exit','Exit','EXIT')) 
    def test_exit(self, parameter):
        with self.assertRaises(ExitGame):
            self.game.print_input(parameter)
    
    @parameterized.expand(('no', 'No', 'NO')) 
    def test_exit_withPlayAgainQuestion(self, parameter):
        with self.assertRaises(ExitGame):
            for counterTimes in range(0,5):
                for counterColumn in range(1,3):
                    self.game.print_input(counterColumn)
            self.game.print_input(parameter)

    @parameterized.expand(('yes', 'Yes', 'YES')) 
    @patch('main.fourInLine.FourInLine.resetBoard')
    def test_playAgain(self, parameter, resetBoard):
        for counterTimes in range(0,5):
            for counterColumn in range(1,3):
                self.game.print_input(counterColumn)
        self.assertEqual(self.game.print_input(parameter), '')
        self.assertEqual(self.game.printStatement, f'\nPlayer 1 select a Column(1-8/exit/reset):  ')
        self.assertTrue(resetBoard.called)

    @parameterized.expand(('es', 'Y', 'YE', '8', '22','2odkd9','exi','¡1¿', '0')) 
    def test_unrecognizedValueOrString(self, parameter):
        self.assertEqual(self.game.print_input(parameter), '')

    @parameterized.expand(('es', 'Y', 'YE', '8', '22','2odkd9','exi','¡1¿', '0')) 
    def test_unrecognizedValueOrString_PlayAgainInstance(self, parameter):
        self.assertEqual(self.game.print_input(parameter), '')

    @parameterized.expand(('reset', 'Reset', 'RESET'))
    @patch('main.fourInLine.FourInLine.resetBoard')
    def test_reset(self, parameter, resetBoard):
        self.assertEqual(self.game.print_input(parameter), '')
        self.assertTrue(resetBoard.called)

    @parameterized.expand(('1', '2', '3', '4', '5', '6', '7', '8'))
    @patch('main.fourInLine.FourInLine.insertToken')
    def test_insertToken(self, parameter, insertToken):
        self.assertEqual(self.game.print_input(parameter), '')
        self.assertTrue(insertToken.called)

    def test_noAvailablePosition(self):
        for rowCounter in range(0,8):
            self.game.print_input(1)
        self.assertEqual(self.game.print_input(1), f'\nThere are no more available positions in column 1\n')
        self.assertEqual(self.game.print_input(1), f'\nThere are no more available positions in column 1\n')

    @patch('main.fourInLine.FourInLine.resetBoard')
    def test_tie(self, resetBoard):
        for columnCounter in range(1,4):
            for rowCounter in range(0,8):
                self.game.print_input(columnCounter)
        for rowCounter in range(0,7):
            switcher = (5,4) if ((rowCounter/2)-(rowCounter//2)) == 0 else (4,5) 
            for columnSelector in(switcher):
                self.game.print_input(columnSelector)
        for columnCounter in range(6,8):
            for rowCounter in range(0,8):
                self.game.print_input(columnCounter)
        self.game.print_input(4)
        for rowCounter in range(0,8):
            self.game.print_input(8)
        self.assertEqual(self.game.print_input(5), '\nTIE! les try again')
        self.assertTrue(resetBoard.called)

    def test_winner(self):
        for counter in range(0,3):
            for columnCounter in range(1,3):
                self.game.print_input(columnCounter)
        self.assertEqual(self.game.print_input(1), '\nPlayer 1 winns!!!\n')
        self.assertEqual(self.game.printStatement, 'Want to play again?(yes/no)  ')