# from http.server import executable
# import unittest
# from unittest.mock import patch
# from src.consoleExecutable import Game

# class ExecutableTestCase(unittest.TestCase):

#     def setUp(self):
#         self.game = Game()

#     @patch('executable.Game.play')
#     @patch('executable.Game.printBoard')
#     def test_boardPrint(self, board, *args):
#         self.game.printBoard()
#         self.assertEqual(self.game.printBoard(), '''
#                                                     +----+----+----+----+----+----+----+----+
#                                                     |    |    |    |    |    |    |    |    |
#                                                     +----+----+----+----+----+----+----+----+
#                                                     |    |    |    |    |    |    |    |    |
#                                                     +----+----+----+----+----+----+----+----+
#                                                     |    |    |    |    |    |    |    |    |
#                                                     +----+----+----+----+----+----+----+----+
#                                                     |    |    |    |    |    |    |    |    |
#                                                     +----+----+----+----+----+----+----+----+
#                                                     |    |    |    |    |    |    |    |    |
#                                                     +----+----+----+----+----+----+----+----+
#                                                     |    |    |    |    |    |    |    |    |
#                                                     +----+----+----+----+----+----+----+----+
#                                                     |    |    |    |    |    |    |    |    |
#                                                     +----+----+----+----+----+----+----+----+
#                                                     |    |    |    |    |    |    |    |    |
#                                                     +----+----+----+----+----+----+----+----+
#                                                     ''')

# if __name__=='__main__':
#     unittest.main()