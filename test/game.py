import unittest
import os
import sys
sys.path.append(os.path.abspath(os.path.dirname(__file__) + '/' + '..'))
import src.game as g
"""
	@moduledoc
	Tests the class Game from the module game
"""

class TestGame(unittest.TestCase):
	def test_initialise_grid(self):
		g.np.random.seed(0) # Set a random seed so the randomness is predictable
		g_initialised = g.initialise_grid(7, 3, 4)
		test = g_initialised == g.np.matrix([[4, 5, 0, 3], [3, 3, 1, 3],[5, 2, 4, 6]])
		self.assertTrue(test.all())
	def test_initialise_control_grid(self):
		pass
	def test_play_color(self):
		pass # , color
	def test_check_neighbors(self):
		pass # , grid, control_grid
	def test_check_neighbor(self):
		pass # , grid, control_grid

if __name__ == '__main__':
	unittest.main()