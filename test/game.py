import unittest
import os
import sys
sys.path.append(os.path.abspath(os.path.dirname(__file__) + '/' + '..'))
import src.game as g
import numpy as np
"""
	@moduledoc
	Tests the class Game from the module game
"""

class TestGame(unittest.TestCase):
	def test_initialise_grid(self):
		g.np.random.seed(0) # Set a random seed so the randomness is predictable
		g_initialised = g.initialise_grid(7, 3, 4)
		test = g_initialised == np.matrix([[4, 5, 0, 3], [3, 3, 1, 3],[5, 2, 4, 6]])
		self.assertTrue(test.all())
	def test_initialise_control_grid(self):
		to_test = g.initialise_control_grid(2,2)
		test = to_test == np.matrix([[True, False], [False, False]])
		self.assertTrue(test.all())

	def test_reward(self):
		checked = np.matrix([[False, False, False, False], [True, False, False, False], [True, True, False, False]])
		self.assertEqual(g.reward(checked), 29)
	def test_play_color(self):
		# Trivial case
		grid = np.matrix([[0,1], [1,1]])
		control_grid = np.matrix([[True, False], [False, False]])
		to_test = g.play_color(1, grid, control_grid)
		# Test the Colors
		self.assertTrue((to_test[0] == np.matrix([[1,1], [1,1]])).all())
		# Test the command
		self.assertTrue((to_test[1] == np.matrix([[True, True], [True, True]])).all())
		self.assertEqual(to_test[2], 29)
		self.assertTrue(to_test[3])
		# More advanced case
		grid = np.matrix([[0,2], [1,1]])
		control_grid = np.matrix([[True, False], [False, False]])
		to_test = g.play_color(1, grid, control_grid)
		# Test the Colors
		self.assertTrue((to_test[0] == np.matrix([[1,2], [1,1]])).all())
		# Test the command
		self.assertTrue((to_test[1] == np.matrix([[True, False], [True, True]])).all())
		self.assertEqual(to_test[2], 19)
		self.assertFalse(to_test[3])

	def test_check_neighbors(self):
		grid = np.matrix([[0,1,2,3,4], [0,0,3,4,5], [1,2,3,4,5]])
		control_grid = np.matrix([[True, False, False, False, False], [False, False, False, False, False], [False, False, False, False, False]])
		to_test = g.check_neighbors(grid, control_grid)
		test = to_test == np.matrix([[False, False, False, False, False], [True, True, False, False, False], [False, False, False, False, False]])
		self.assertTrue(test.all())
	def test_check_neighbor(self):
		grid = np.matrix([[0,1,2,3,4], [0,0,3,4,5], [1,2,3,4,5]])
		control_grid = np.matrix([[True, False, False, False, False], [False, False, False, False, False], [False, False, False, False, False]])
		to_test = g.check_neighbor(grid, control_grid)
		test = to_test == np.matrix([[False, False, False, False, False], [True, False, False, False, False], [False, False, False, False, False]])
		self.assertTrue(test.all())
	def test_has_game_ended(self):
		state = np.matrix([[True, False], [False, True]])
		self.assertFalse(g.has_game_ended(state))

		state = np.matrix([[True, True, True], [True, True, True]])
		self.assertTrue(g.has_game_ended(state))
if __name__ == '__main__':
	unittest.main()